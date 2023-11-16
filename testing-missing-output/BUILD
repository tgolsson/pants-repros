python_sources(
    name="root",
)

python_tests(
    name="tests0",
)


TOOLS = {
    "pytest": [
        "pytest-cov!=2.12.1,<3.1,>=2.12",
        "pytest-xdist<3,>=2.5",
        "pytest==7.0.*",
        "pytest-platform-markers",
        "pytest-rerunfailures",
        "pytest-benchmark==4.0.0",
    ]
}

for tool, reqs in TOOLS.items():
    python_requirement(
        name=tool,
        requirements=reqs,
        resolve=tool,
    )
