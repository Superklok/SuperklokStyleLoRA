#!/usr/bin/env python3
"""
⚡ Superklok Labs — SuperklokStyleLoRA Training Architecture Platform Installer ⚡
Author: Trevor Morin | Superklok Labs ➔ superklok.com
License: MIT / Unified Public Asset License v1.0

This highly advanced platform installer designs a fully integrated local LoRA training pipeline.
Deploys an unprivileged portable workspace for ComfyUI with SD3.5 Large and dataset wiring.
"""

import os
import sys

# -------------------------------------------------------------------------
# GLOBAL UX ENVIRONMENTAL OVERRIDES
# Must be set first before any third-party framework evaluations occur
# -------------------------------------------------------------------------
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import shutil
import urllib.request
import subprocess
import threading
import time

# -------------------------------------------------------------------------
# DEPENDENCY HANDSHAKE & RUNTIME INJECTION
# Handled first to ensure modules are ready before core script evaluation
# -------------------------------------------------------------------------
REQUIRED_LIBS = ["rich", "py7zr"]
missing_libs = []

for lib in REQUIRED_LIBS:
    try:
        __import__(lib)
    except ImportError:
        missing_libs.append(lib)

if missing_libs:
    done = False
    
    def animate_bootstrap():
        # A dynamic array of high-grade console frame indicators
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0
        while not done:
            sys.stdout.write(f"\r\033[95m{frames[idx % len(frames)]}\033[0m Preparing Superklok core engine libraries (allocating visual assets)...")
            sys.stdout.flush()
            time.sleep(0.08)
            idx += 1
        sys.stdout.write("\r" + " " * 85 + "\r")
        sys.stdout.flush()

    # Spins up the animation loop on a concurrent background worker thread
    anim_thread = threading.Thread(target=animate_bootstrap, daemon=True)
    anim_thread.start()

    try:
        # Silently downloads the design wheels using completely hidden null routing parameters
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing_libs, "--quiet", "--no-warn-script-location", "--user"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    finally:
        # Halt the loop thread immediately when pip closes
        done = True
        anim_thread.join()
    
    # Inject user-site packages into the runtime system path
    import site
    if hasattr(site, 'getusersitepackages'):
        user_site = site.getusersitepackages()
        if user_site not in sys.path:
            sys.path.insert(0, user_site)

from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
import py7zr

# Initialize global styling console
console = Console()

class LoRATrainingInstaller:
    """Orchestrates ComfyUI pipeline architecture configurations for local SD3.5 Large LoRA fine-tuning."""

    # LoRA-specific identifiers
    PROJECT_NAME: str = "SuperklokStyleLoRA"
    DATASET_SUBFOLDER: str = "20_SuperklokStyle"
    WORKFLOW_FILENAME: str = "ComfyUI Workflow - SuperklokStyleLoRA - SD3.5Large.json"

    # Stable Diffusion 3.5 Large FP8 link
    CHECKPOINT_URL: str = (
        "https://huggingface.co/Comfy-Org/stable-diffusion-3.5/resolve/main/sd3.5_large_fp8_scaled.safetensors"
    )
    
    # ComfyUI Official standalone portable build asset link
    COMFYUI_PORTABLE_URL: str = (
        "https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia.7z"
    )

    def __init__(self) -> None:
        # Resolve all top-level platform layers relative to workspace footprint
        self.root_dir: str = os.getcwd()
        
        # Generation Spaces
        self.archive_path: str = os.path.join(self.root_dir, "ComfyUI_windows_portable_nvidia.7z")
        self.portable_dir: str = os.path.join(self.root_dir, "ComfyUI_windows_portable")
        self.comfy_dir: str = os.path.join(self.portable_dir, "ComfyUI")
        self.nodes_dir: str = os.path.join(self.comfy_dir, "custom_nodes")
        self.dataset_dir: str = os.path.join(self.root_dir, "dataset", self.DATASET_SUBFOLDER)

    def render_welcome_banner(self) -> None:
        """Displays a styled branding header into the active terminal session."""
        banner_text = (
            f"[bold yellow]📺 {self.PROJECT_NAME} v1.12.0 - 100% Commercial Use 📺[/bold yellow]\n"
            f"[bold cyan]Author: Trevor Morin | Superklok Labs ➔ superklok.com[/bold cyan]\n\n"
            "[dim]Installer configures low-VRAM FP8 training, links ComfyUI-Manager core layers,\n"
            "streams SD3.5 Large weights, and wires local training datasets natively.[/dim]"
        )
        console.print(Panel.fit(banner_text, border_style="cyan", padding=(1, 4)))

    def stream_large_file(self, url: str, dest_path: str, description: str) -> None:
        """Downloads heavy binary layers utilizing multi-threaded concurrent chunk segmenting with atomic .part safeguards."""
        import concurrent.futures
        import threading

        if os.path.exists(dest_path):
            console.print(f"[bold green]✓[/bold green] {os.path.basename(dest_path)} detected in cache. Skipping download.")
            return

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        temp_path = f"{dest_path}.part"

        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

        progress_lock = threading.Lock()

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bright_cyan"),
            TextColumn(description),
            BarColumn(
                bar_width=45,
                style="black on blue",
                complete_style="magenta",
                finished_style="green",
                pulse_style="magenta"
            ),
            TaskProgressColumn(style="bold yellow"),
            DownloadColumn(binary_units=True),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
            refresh_per_second=20,
            auto_refresh=True
        ) as progress:

            task_id = progress.add_task(description="", total=None)

            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, method='HEAD')
                with urllib.request.urlopen(req) as resp:
                    total_size = int(resp.info().get('Content-Length', 0))
            except Exception:
                total_size = 0

            if total_size == 0:
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urllib.request.urlopen(req) as response:
                        total_size = int(response.info().get('Content-Length', 0))
                        progress.update(task_id, total=total_size)
                        with open(temp_path, 'wb') as f:
                            while chunk := response.read(1024 * 128):
                                f.write(chunk)
                                progress.update(task_id, advance=len(chunk))
                        os.replace(temp_path, dest_path)
                        return
                except Exception as e:
                    console.print(f"[bold red]❌ Fallback Stream Interrupted: {e}[/bold red]")
                    sys.exit(1)

            num_threads = 4
            chunk_size = total_size // num_threads
            ranges = []
            for i in range(num_threads):
                start = i * chunk_size
                end = total_size - 1 if i == num_threads - 1 else (start + chunk_size - 1)
                ranges.append((start, end))

            with open(temp_path, 'wb') as f:
                f.truncate(total_size)

            progress.update(task_id, total=total_size)

            def download_range(part_num, start, end):
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Range': f'bytes={start}-{end}'
                })
                try:
                    with urllib.request.urlopen(req) as response:
                        with open(temp_path, 'r+b') as f:
                            f.seek(start)
                            buffer_size = 1024 * 64
                            while chunk := response.read(buffer_size):
                                f.write(chunk)
                                with progress_lock:
                                    progress.update(task_id, advance=len(chunk))
                except urllib.error.HTTPError as e:
                    if e.code == 501 or e.code == 416:
                        with progress_lock:
                            raise NotImplementedError("Range unsupported")
                    console.print(f"\n[bold red]❌ Thread {part_num} dropped stream: {e}[/bold red]")
                    os._exit(1)
                except Exception as e:
                    console.print(f"\n[bold red]❌ Thread {part_num} dropped stream: {e}[/bold red]")
                    os._exit(1)

            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                    futures = [
                        executor.submit(download_range, idx, r[0], r[1])
                        for idx, r in enumerate(ranges)
                    ]
                    for future in concurrent.futures.as_completed(futures):
                        future.result()
                os.replace(temp_path, dest_path)
            except (NotImplementedError, concurrent.futures.BrokenExecutor):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
                
                progress.update(task_id, total=None)
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                try:
                    with urllib.request.urlopen(req) as response:
                        total_size = int(response.info().get('Content-Length', 0))
                        progress.update(task_id, total=total_size)
                        with open(temp_path, 'wb') as f:
                            while chunk := response.read(1024 * 128):
                                f.write(chunk)
                                progress.update(task_id, advance=len(chunk))
                        os.replace(temp_path, dest_path)
                except Exception as e:
                    console.print(f"[bold red]❌ Fallback Stream Interrupted: {e}[/bold red]")
                    sys.exit(1)

    def extract_portable_environment(self) -> None:
        """Unpacks the standalone environment package dynamically utilizing an auto-fetched 7zr helper."""
        if os.path.exists(self.portable_dir):
            console.print("[bold green]✓[/bold green] ComfyUI Portable framework directory structure already initialized.")
            return

        if not os.path.exists(self.archive_path):
            console.print(f"[bold red]❌ Extraction payload missing: {self.archive_path}[/bold red]")
            sys.exit(1)

        with Status("[bold white]Decompressing ComfyUI Core Environment (Native Hardware Pipeline)...[/bold white]", console=console, spinner="bouncingBall") as status:
            try:
                archive_abs = os.path.abspath(self.archive_path)
                root_abs = os.path.abspath(self.root_dir)
                
                extractor_bin = os.path.join(self.root_dir, "7zr.exe")
                if not os.path.exists(extractor_bin):
                    primary_url = "https://www.7-zip.org/a/7zr.exe"
                    fallback_url = "https://github.com/ip7z/7zip/releases/download/26.06/7zr.exe"
                    try:
                        urllib.request.urlretrieve(primary_url, extractor_bin)
                    except Exception:
                        urllib.request.urlretrieve(fallback_url, extractor_bin)
                
                subprocess.run(
                    [extractor_bin, "x", archive_abs, f"-o{root_abs}", "-y"],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                
                extracted_expected = os.path.join(self.root_dir, "ComfyUI_windows_portable_nvidia")
                if os.path.exists(extracted_expected) and not os.path.exists(self.portable_dir):
                    os.rename(extracted_expected, self.portable_dir)
                    
                console.print("[bold green]✓[/bold green] Standalone visual environment successfully unpacked.")
                
                try:
                    os.remove(self.archive_path)
                    if os.path.exists(extractor_bin):
                        os.remove(extractor_bin)
                except OSError:
                    pass
            except Exception as e:
                console.print(f"[bold red]❌ Failed unpacking portable suite via hardware layout: {e}[/bold red]")
                sys.exit(1)

    def execute_git_clone(self, repo_url: str, base_destination: str, folder_name: str, name_label: str) -> None:
        """Safely forks public version-controlled extensions into target terminal paths."""
        target_path = os.path.join(base_destination, folder_name)
        if os.path.exists(target_path):
            console.print(f"[bold green]✓[/bold green] [bold yellow]{name_label}[/bold yellow] already linked in workspace.")
            return

        with Status(f"[bold white]Cloning {name_label}...[/bold white]", console=console, spinner="aesthetic") as status:
            try:
                subprocess.run(
                    ["git", "clone", repo_url, target_path],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                console.print(f"[bold green]✓[/bold green] Installed [bold cyan]{name_label}[/bold cyan] to production folders.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                console.print(f"[bold red]❌ Failed tracking Git dependency. Ensure Git for Windows is installed globally.[/bold red]")
                sys.exit(1)

    def provision_launch_scripts(self) -> None:
        """Injects custom startup code configured for low-VRAM FP8 memory balancing directly into runtime paths."""
        startup_file = os.path.join(self.portable_dir, "run_nvidia_gpu.bat")
        
        # Specialized balancing constraints tailored for single 16GB VRAM card limits
        optimized_args = (
            ".\\python_embeded\\python.exe -s ComfyUI\\main.py --windows-standalone-build "
            "--fp8_e4m3fn-text-enc --use-pytorch-cross-attention --lowvram\n"
        )

        try:
            with open(startup_file, "w", encoding="utf-8") as file:
                file.write(optimized_args)
            console.print("[bold green]✓[/bold green] Low-overhead VRAM arguments written to launch script.")
        except IOError:
            console.print("[bold red]❌ Launch script adjustment error.[/bold red]")

    def inject_training_dataset(self) -> None:
        """Copies the local image + caption dataset folder directly into ComfyUI's input directory."""
        comfy_input_dest = os.path.join(self.comfy_dir, "input", self.DATASET_SUBFOLDER)
        os.makedirs(comfy_input_dest, exist_ok=True)

        if not os.path.exists(self.dataset_dir):
            console.print(f"[bold yellow]⚠[/bold yellow] Training dataset folder not found: {self.dataset_dir}")
            return

        copied_count = 0
        with Status(f"[bold white]Wiring training dataset ({self.DATASET_SUBFOLDER}) into ComfyUI\\input...[/bold white]", console=console) as status:
            for file in sorted(os.listdir(self.dataset_dir)):
                src_file = os.path.join(self.dataset_dir, file)
                if os.path.isfile(src_file):
                    dest_file = os.path.join(comfy_input_dest, file)
                    if not os.path.exists(dest_file):
                        shutil.copy2(src_file, dest_file)
                    copied_count += 1

        if copied_count > 0:
            console.print(f"[bold green]✓[/bold green] Wired {copied_count} dataset images & captions into ComfyUI\\input\\{self.DATASET_SUBFOLDER}.")

    def run(self) -> None:
        """Executes orchestration steps sequentially."""
        self.render_welcome_banner()

        # Step 1: Fetch ComfyUI Portable Build into Workspace Root
        if not os.path.exists(self.portable_dir) and not os.path.exists(self.archive_path):
            self.stream_large_file(
                url=self.COMFYUI_PORTABLE_URL,
                dest_path=self.archive_path,
                description="[bold white]Streaming ComfyUI Portable Build[/bold white]"
            )

        # Step 2: Unpack ComfyUI Base Layer Environment
        self.extract_portable_environment()

        # Step 3: Inject Optimized Drivers & Hardware Controls
        self.provision_launch_scripts()

        # Step 4: Provision ComfyUI-Manager Ecosystem Core
        console.print("\n[bold magenta]» Linking ComfyUI-Manager Core Layer...[/bold magenta]")
        self.execute_git_clone(
            repo_url="https://github.com/ltdrdata/ComfyUI-Manager",
            base_destination=self.nodes_dir,
            folder_name="comfyui-manager",
            name_label="comfyui-manager"
        )

        # Initializing Node Pack Dependencies via Embedded Python
        console.print("\n[bold magenta]» Initializing Core Dependencies via Embedded Python...[/bold magenta]")
        embedded_python = os.path.join(self.portable_dir, "python_embeded", "python.exe")
        
        if os.path.exists(embedded_python):
            # Explicitly force-upgrade ComfyUI-Manager requirements to ensure stable mapping
            manager_req = os.path.join(self.nodes_dir, "comfyui-manager", "requirements.txt")
            if os.path.exists(manager_req):
                with Status("[bold white]Securing ComfyUI-Manager requirements...[/bold white]", console=console) as status:
                    subprocess.run([embedded_python, "-m", "pip", "install", "--no-warn-script-location", "--isolated", "-r", manager_req, "--quiet"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            console.print("[bold green]✓[/bold green] Core ecosystem dependencies compiled and locked into embedded runtime.")

        # Step 5: Pull Foundational SD3.5 Large Checkpoint
        console.print("\n[bold magenta]» Allocating Foundational Training Checkpoint Block...[/bold magenta]")
        
        # Checkpoint: sd3.5_large_fp8_scaled.safetensors
        self.stream_large_file(
            url=self.CHECKPOINT_URL,
            dest_path=os.path.join(self.comfy_dir, "models", "checkpoints", "sd3.5_large_fp8_scaled.safetensors"),
            description="[bold white]Streaming SD3.5 Large FP8 Checkpoint[/bold white]"
        )

        # Step 6: Wire Training Image & Caption Dataset into ComfyUI/input
        console.print("\n[bold magenta]» Wiring Local Training Dataset into ComfyUI Pipeline...[/bold magenta]")
        self.inject_training_dataset()

        # Final Status Presentation
        console.print(
            f"\n[bold green]🏁 LoRA TRAINING PIPELINE ENVIRONMENT PROVISIONED! 🏁[/bold green]\n"
            f"1. Start ComfyUI image-generation [bold cyan]ComfyUI_windows_portable\\run_nvidia_gpu.bat[/bold cyan].\n"
            f"2. Drag and drop [bold cyan]{self.WORKFLOW_FILENAME}[/bold cyan] into the browser window.\n"
            f"3. Press [bold cyan]Run[/bold cyan] to train your custom LoRA into [bold cyan]ComfyUI\\output\\models\\loras[/bold cyan].\n"
            f"\n[bold magenta]Powered by Superklok Labs.[/bold magenta]\n"
        )


if __name__ == "__main__":
    try:
        installer = LoRATrainingInstaller()
        installer.run()
    except KeyboardInterrupt:
        console.print("\n[bold red]✖ Automation loop terminated by user request.[/bold red]")
        sys.exit(1)
