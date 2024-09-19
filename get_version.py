import importlib.metadata

def get_package_version(package_name):
    try:
        version = importlib.metadata.version(package_name)
        return f"{package_name}=={version}"
    except importlib.metadata.PackageNotFoundError:
        return(f"{package_name} is not installed")

# Example usage
print(' '.join([get_package_version(package) for package in ['chromadb','langchain','sentence-transformers','flask_restful']]))

