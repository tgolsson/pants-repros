TORCH_VERSION = "1.12.0"
CUDA_VERSION = "cu116"

TORCH_VARIANTS = {
    "base": f"=={TORCH_VERSION},!={TORCH_VERSION}+cpu,!={TORCH_VERSION}+{CUDA_VERSION}",
}

MODULE_MAPPINGS = {
    "pillow": ["PIL"],

}

for resolve in ["base"]:
    python_requirements(
        name=resolve,
        module_mapping=MODULE_MAPPINGS,
        source="requirements.txt",
        resolve=resolve,
    )

    python_requirement(
        name=f"torch-{resolve}",
        requirements=[f"torch{TORCH_VARIANTS[resolve]}"],
        resolve=resolve,
        modules=["torch"],
    )
