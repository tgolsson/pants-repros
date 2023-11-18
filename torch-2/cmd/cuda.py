from __future__ import annotations

import ctypes
import dataclasses
import functools
import logging

# UNCOMMENT THIS LINE TO FIX
# import nvidia
import torch

torch.cuda.init()
assert torch.cuda.is_initialized()
logger = logging.getLogger(__name__)

# From cuda.h
CUDA_SUCCESS = 0
CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT = 16
CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR = 39
CU_DEVICE_ATTRIBUTE_CLOCK_RATE = 13
CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE = 36


def sm_to_cores(major, minor):
    # Returns the number of CUDA cores per multiprocessor for a given
    # Compute Capability version. There is no way to retrieve that via
    # the API, so it needs to be hard-coded.
    # See _ConvertSMVer2Cores in helper_cuda.h in NVIDIA's CUDA Samples.
    return {
        (1, 0): 8,  # Tesla
        (1, 1): 8,
        (1, 2): 8,
        (1, 3): 8,
        (2, 0): 32,  # Fermi
        (2, 1): 48,
        (3, 0): 192,  # Kepler
        (3, 2): 192,
        (3, 5): 192,
        (3, 7): 192,
        (5, 0): 128,  # Maxwell
        (5, 2): 128,
        (5, 3): 128,
        (6, 0): 64,  # Pascal
        (6, 1): 128,
        (6, 2): 128,
        (7, 0): 64,  # Volta
        (7, 2): 64,
        (7, 5): 64,  # Turing
        (8, 0): 64,  # Ampere
        (8, 6): 64,
    }.get((major, minor), 0)


class CudaContext:
    class Device:
        def __init__(self, cuda, device, context):
            self.cuda = cuda
            self.device = device
            self.context = context

        def __del__(self):
            self.cuda.cuCtxDetach(self.context)

        @functools.cached_property
        def name(self) -> str:
            name = b" " * 100
            result = ctypes.c_int()

            result = self.cuda.cuDeviceGetName(name, 100, self.device)
            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuDeviceGetName failed: %s", error_str.value)
                return None

            return name.split(b"\0", 1)[0].decode()

        @functools.cached_property
        def compute_capability(self) -> (int, int):
            cc_major = ctypes.c_int()
            cc_minor = ctypes.c_int()
            result = ctypes.c_int()

            result = self.cuda.cuDeviceComputeCapability(
                ctypes.byref(cc_major), ctypes.byref(cc_minor), self.device
            )
            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuDeviceComputeCapability failed: %s", error_str.value)
                return None

            return (cc_major.value, cc_minor.value)

        @functools.cached_property
        def multiprocessors(self) -> int:
            mp = ctypes.c_int()
            result = ctypes.c_int()

            result = self.cuda.cuDeviceGetAttribute(
                ctypes.byref(mp), CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, self.device
            )
            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuDeviceGetAttribute failed: %s", error_str.value)

                return None

            return mp.value

        @functools.cached_property
        def max_threads_per_multiprocessor(self) -> int:
            mp = ctypes.c_int()
            result = ctypes.c_int()

            result = self.cuda.cuDeviceGetAttribute(
                ctypes.byref(mp),
                CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR,
                self.device,
            )
            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuDeviceGetAttribute failed: %s", error_str.value)

                return None

            return mp.value

        @functools.cached_property
        def clock_rate(self) -> int:
            mp = ctypes.c_int()
            result = ctypes.c_int()

            result = self.cuda.cuDeviceGetAttribute(
                ctypes.byref(mp), CU_DEVICE_ATTRIBUTE_CLOCK_RATE, self.device
            )
            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuDeviceGetAttribute failed: %s", error_str.value)

                return None

            return mp.value

        @functools.cached_property
        def memory_clock_rate(self) -> int:
            mp = ctypes.c_int()
            result = ctypes.c_int()

            result = self.cuda.cuDeviceGetAttribute(
                ctypes.byref(mp), CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE, self.device
            )
            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuDeviceGetAttribute failed: %s", error_str.value)

                return None

            return mp.value

        @functools.cached_property
        def total_memory(self) -> int:
            mem = ctypes.c_size_t()
            result = ctypes.c_int()

            result = self.cuda.cuDeviceTotalMem(ctypes.byref(mem), self.device)
            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuDeviceTotalMem failed: %s", error_str.value)
                return None

            return mem.value

        @functools.cached_property
        def cuda_cores(self) -> int:
            (cc_major, cc_minor) = self.compute_capability
            return self.multiprocessors * sm_to_cores(cc_major, cc_minor)

        def memory_info(self) -> (int, int):
            free = ctypes.c_size_t()
            total = ctypes.c_size_t()
            result = ctypes.c_int()

            try:
                result = self.cuda.cuMemGetInfo_v2(
                    ctypes.byref(free), ctypes.byref(total)
                )
            except AttributeError:
                result = self.cuda.cuMemGetInfo(ctypes.byref(free), ctypes.byref(total))

            if result != CUDA_SUCCESS:
                error_str = ctypes.c_char_p()
                self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
                logging.error("cuMemGetInfo failed: %s", error_str.value)
                return None

            return (free.value, total.value)

        def memory_fraction(self) -> float:
            (free, total) = self.memory_info()
            return 1.0 - free / total

        @functools.cached_property
        def info(self) -> CudaDeviceInfo:
            return CudaDeviceInfo(
                name=self.name,
                compute_capability=self.compute_capability,
                multiprocessors=self.multiprocessors,
                max_threads_per_multiprocessor=self.max_threads_per_multiprocessor,
                clock_rate=self.clock_rate,
                memory_clock_rate=self.memory_clock_rate,
                total_memory=self.total_memory,
                cuda_cores=self.cuda_cores,
                memory_usage=self.memory_fraction(),
            )

    def __init__(self):
        for lib in ["libcuda.so", "libcuda.so.1", "libcuda.dylib"]:
            try:
                self.cuda = ctypes.CDLL(lib)
                break
            except OSError as exc:
                print(exc)
                pass
        else:
            raise RuntimeError("Could not find libcuda.so or libcuda.dylib")

        device_count = ctypes.c_int()
        error_str = ctypes.c_char_p()

        result = self.cuda.cuInit(0)
        if result != CUDA_SUCCESS:
            self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
            logging.error(
                "cuInit failed with error code %d: %s", result, error_str.value.decode()
            )
            return None

        result = self.cuda.cuDeviceGetCount(ctypes.byref(device_count))
        if result != CUDA_SUCCESS:
            self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
            logging.error(
                "cuDeviceGetCount failed with error code %d: %s",
                result,
                error_str.value.decode(),
            )
            return None

        self.device_count = device_count.value

    def get_device(self, index: int) -> CudaContext.Device | None:
        if self.device_count == 0:
            return None

        device = ctypes.c_int()
        context = ctypes.c_void_p()
        error_str = ctypes.c_char_p()

        result = self.cuda.cuDeviceGet(ctypes.byref(device), index)
        if result != CUDA_SUCCESS:
            self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
            logging.error(
                "cuDeviceGet failed with error code %d: %s",
                result,
                error_str.value.decode(),
            )
            return None

        try:
            result = self.cuda.cuCtxCreate_v2(ctypes.byref(context), 0, device)
        except AttributeError:
            result = self.cuda.cuCtxCreate(ctypes.byref(context), 0, device)

        if result != CUDA_SUCCESS:
            self.cuda.cuGetErrorString(result, ctypes.byref(error_str))
            logging.error(
                "cuCtxCreate failed with error code %d: %s",
                result,
                error_str.value.decode(),
            )
            return None

        return CudaContext.Device(self.cuda, device, context)

    def info(self) -> CudaInfo:
        devices = []
        for i in range(self.device_count):
            device = self.get_device(i)
            if device is not None:
                devices.append(device.info)

        return CudaInfo(devices)


@dataclasses.dataclass
class CudaDeviceInfo:
    name: str
    compute_capability: str
    multiprocessors: int
    max_threads_per_multiprocessor: int
    clock_rate: int
    memory_clock_rate: int
    total_memory: int
    cuda_cores: int
    memory_usage: float


@dataclasses.dataclass
class CudaInfo:
    devices: list[CudaDeviceInfo]


def debug_print():
    import subprocess

    try:
        output = subprocess.check_output(["nvidia-smi"], stderr=subprocess.STDOUT)

        logging.info("Nvidia-SMI output:")
        print(output.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        output = e
        logging.error("nvidia-smi failed with error code %d", output.returncode)
        if output.stdout:
            print("stdout:")
            print(output.stdout.decode("utf-8"))
        if output.stderr:
            print("stderr:")
            print(output.stderr.decode("utf-8"))

    except FileNotFoundError:
        logging.error("nvidia-smi not found")

    try:
        output = subprocess.check_output(
            ["nvcc", "--version"], stderr=subprocess.STDOUT
        )

        logging.info("nvcc output:")
        print(output.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        output = e
        logging.error("nvcc failed with error code %d", output.returncode)
        if output.stdout:
            print("stdout:")
            print(output.stdout.decode("utf-8"))
        if output.stderr:
            print("stderr:")
            print(output.stderr.decode("utf-8"))

    except FileNotFoundError:
        logging.error("nvcc not found")

    try:
        ctx = CudaContext()
        info = ctx.info()

        logging.info("CUDA info (%s devices):", len(info.devices))
        for device in info.devices:
            print(f'Device: "{device.name}"')
            print(f"  Compute capability: {device.compute_capability}")
            print(f"  Multiprocessors:    {device.multiprocessors}")
            print(f"  Warp size:          {device.max_threads_per_multiprocessor}")
            print(f"  Clock rate:         {device.clock_rate}")
            print(f"  Memory clock rate:  {device.clock_rate}")
            print(f"  Total memory:       {device.total_memory}")
            print(f"  Cuda cores: {device.cuda_cores}")
    except Exception as e:
        logging.error("Failed to get CUDA info: %s", e)


if __name__ == "__main__":
    print(torch.version.__version__)
    debug_print()
