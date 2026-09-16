import re
text = open('src/CursorBridge.py', 'r', encoding='utf-8').read()
# Look for path matching patterns
routes = re.findall(r'path\s*==\s*["\']([^"\']+)["\']', text)
print('Routes:', routes)

# Also look for endpoint definitions
endpoints = re.findall(r'["\'](/[^"\']+)["\']', text)
print('Endpoints:', endpoints[:50])