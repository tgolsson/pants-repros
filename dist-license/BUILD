resources(
    name="package_data", sources=["README.md", "LICENSE.txt"]
)

python_distribution(
    name="package",
    dependencies=[
        ":package_data",
        "//src/py/mylib:mylib",
    ],
    provides=python_artifact(
        name="package",
        version="0.1.0",
        long_description_content_type="markdown",
    ),
    generate_setup=True,
    long_description_path="README.md",
)
