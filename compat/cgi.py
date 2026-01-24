# Compatibility shim for Python 3.13 - minimal cgi module
import email
import urllib.parse

class FieldStorage:
    def __init__(self, *args, **kwargs):
        self.list = []
    
    def getvalue(self, key, default=None):
        return default
    
    def getfirst(self, key, default=None):
        return default
    
    def getlist(self, key):
        return []

def parse_header(value):
    """Parse a header value - returns (value, params_dict)"""
    if not value:
        return '', {}
    
    # Use email.headerregistry to parse
    try:
        # For simple cases, split on semicolon
        parts = value.split(';', 1)
        main_value = parts[0].strip()
        params = {}
        
        if len(parts) > 1:
            # Parse parameters
            param_string = parts[1]
            for param in param_string.split(';'):
                if '=' in param:
                    key, val = param.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"\'')
                    params[key] = val
        
        return main_value, params
    except Exception:
        return value, {}

def parse_multipart(fp, pdict, encoding="utf-8", errors="replace"):
    """Parse multipart form data"""
    return {}, b""

def valid_boundary(boundary):
    """Check if boundary is valid"""
    if not boundary:
        return False
    # Basic validation - boundary should be alphanumeric with some special chars
    import re
    # Handle both bytes and string
    if isinstance(boundary, bytes):
        boundary = boundary.decode('utf-8', errors='ignore')
    return bool(re.match(r'^[a-zA-Z0-9\'()+_,-./:=? ]+$', boundary))

# Minimal exports that Django might need
escape = urllib.parse.quote
