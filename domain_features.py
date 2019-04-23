# prothom alo features
def hardRules(url):
    
    if 'quora' in url:
        if not url.startswith('https://bn.'):
            return True
    else:
        if url.startswith('https://profiles'):
            return True
        if url.startswith('https://en.'):
            return True
        if url.startswith('http://en.'):
            return True
        if 'UserLogin' in url:
            return True
        if 'Contributions' in url:
                return True
        if 'Log' in url:
                return True
        if url.endswith('.jpg'):
            return True

