
python_sources(
    sources=[
        "cuda.py",
    ],
)

pex_binary(
    name="packed",
    entry_point="cuda",
    resolve="torch2",
    execution_mode="venv",
    layout="packed",
)


pex_binary(
    name="loose",
    entry_point="cuda",
    resolve="torch2",
    execution_mode="venv",
    layout="loose",
)


pex_binary(
    name="zipapp",
    entry_point="cuda",
    resolve="torch2",
    execution_mode="venv",
    layout="zipapp",
)
