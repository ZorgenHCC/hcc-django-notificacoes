import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    content_readme = file.read()

setuptools.setup(
    name='hcc',
    version='0.1',
    author='Tomás Loureiro Gomes',
    author_email='administrativo@tomas.dev.br',
    description='Pacote para utilizar as notificações da HCC',
    long_description=content_readme,
    long_description_content_type="text/markdown",
    url='https://github.com/ZorgenHCC/hcc-django-notificacoes',
    project_urls={
        "Bug Tracker": "https://github.com/ZorgenHCC/hcc-django-notificacoes/issues"
    },
    license='MIT',
    packages=['hcc'],
    install_requires=['requests'],
)
