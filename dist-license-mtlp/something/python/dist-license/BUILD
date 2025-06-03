python_sources(name="src")
resources(name="package_data", sources=["README.md", "LICENSE.txt"])

python_distribution(
    name="dist-license",
    dependencies=[
        ":package_data",
        ":src",
    ],
    provides=python_artifact(
        name="dist-license",
        version="0.1.1",
        long_description_content_type="text/markdown",
        license_files=[f"dist-license/LICENSE.txt"],
    ),
    generate_setup=True,
    # This actually has to be relative to build-root, so we specify it
    # with a macro for the prefix.
    long_description_path=f"{build_file_dir()}/README.md",
)
