"""Regression coverage for rejecting silently ignored schema constraints."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_card_forge import load_schema, schema_capability_errors


class SchemaCapabilitiesTests(unittest.TestCase):
    def test_unsupported_root_assertion(self):
        self.assertIn("unsupported schema keyword 'minLength'", schema_capability_errors({"type": "string", "minLength": 3})[0])

    def test_absent_property_constraint_is_still_checked(self):
        errors = schema_capability_errors({"properties": {"optional": {"pattern": "x"}}})
        self.assertIn("properties.optional", errors[0])

    def test_nested_array_constraint(self):
        self.assertTrue(schema_capability_errors({"items": {"properties": {"x": {"minimum": 0}}}}))

    def test_property_names_and_annotation_values_are_not_keywords(self):
        schema = {"properties": {"minimum": {"type": "number"}, "allOf": {"type": "string"}},
                  "default": {"pattern": "data"}, "examples": [{"minimum": 2}], "enum": [{"const": "data"}]}
        self.assertEqual(schema_capability_errors(schema), [])

    def test_unsupported_forms(self):
        for schema in ({"additionalProperties": {"type": "string"}}, {"items": []}, {"items": False}, {"properties": []}, {"type": "bogus"}, {"required": "x"}, {"enum": "x"}):
            with self.subTest(schema=schema):
                self.assertTrue(schema_capability_errors(schema))

    def test_load_schema_enforces_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "schema.json"
            path.write_text(json.dumps({"allOf": [{"type": "string"}]}))
            with self.assertRaisesRegex(RuntimeError, "unsupported schema keyword 'allOf'"):
                load_schema(Path(tmp), path.name)


if __name__ == "__main__":
    unittest.main()
