python_requirement(
    name="torch_restricted",
    requirements=["torch==1.11.0,!=1.11.0+cpu,!=1.11.0+cu115"],
    resolve="valid",
)

python_requirement(
    name="torch_any",
    requirements=["torch==1.11.0"],
    resolve="broken",
)

python_requirement(
    name="torch_cpu",
    requirements=["torch==1.11.0+cpu"],
    resolve="cpu",
)

python_requirement(
    name="torch_gpu",
    requirements=["torch==1.11.0+cu115"],
    resolve="gpu",
)
