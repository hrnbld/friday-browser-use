"""
Structured output extraction from HTML
"""

import re
from typing import Any, Type, Optional
from pydantic import BaseModel, create_model


class SchemaExtractor:
    """
    Extract structured data from HTML using schema definitions.
    
    Usage:
        class Product(BaseModel):
            name: str
            price: str
            
        extractor = SchemaExtractor(Product)
        result = extractor.extract_from_html(html)
    """
    
    def __init__(self, schema: Type[BaseModel]):
        self.schema = schema
        
    def extract_from_html(self, html: str) -> dict:
        """Extract structured data from HTML"""
        # Simple extraction based on schema fields
        data = {}
        
        for field_name, field_type in self.schema.model_fields.items():
            # Try to find element with this field name
            field_lower = field_name.lower().replace('_', ' ')
            
            # Look for patterns in HTML
            patterns = [
                rf'<[^>]*>([^<]*]{field_lower}[^<]*)<',
                rf'{field_lower}[^:]*:\s*([^<\\n]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html, re.I)
                if match:
                    data[field_name] = match.group(1).strip()
                    break
                    
        return data
    
    @staticmethod
    def create_schema_from_fields(fields: dict) -> Type[BaseModel]:
        """Create Pydantic schema from field definitions"""
        return create_model("DynamicSchema", **fields)


def extract_schema(schema_class: Type[BaseModel], html: str) -> dict:
    """Helper function to extract data"""
    extractor = SchemaExtractor(schema_class)
    return extractor.extract_from_html(html)
