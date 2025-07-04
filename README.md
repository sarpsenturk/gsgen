# GSGEN: Text-to-3D using Gaussian Splatting

This repository is a fork of the original [GSGEN: Text-to-3D using Gaussian Splattng](https://gsgen3d.github.io) project.

### [Paper](https://arxiv.org/abs/2309.16585) | [Project Page](https://gsgen3d.github.io/) | [Original Repository](https://github.com/gsgen3d/gsgen)

## Requirements

- Python 3.10
- CUDA 12.8
- GCC 11

Google Colab is not supported out of the box due to CUDA and Python version mismatches.

## Getting Started

0. Create virtual environment:

```
python3.10 -m venv .venv
source .venv/bin/activate
```

1. Install the requirements:

```
pip install -r requirements.txt
```

2. Build the extension for Gaussian Splatting:

```
cd gs
./build.sh
```

3. Start training!

```
./train.sh "<prompt>"
```

## Exporting

You can easily export the training results to a .ply file:

```
./export.sh <ckpt_path>
```

Checkpoints are stored in the `checkpoints/` directory. 

Export results are stored in the `exports/ply/` directory.

## Flask API

Run the Flask API with:

```
flask --app app run
```

This will run the development server on `localhost:5000`

### Environment Variables

The API requires a connection to Supabase, and therefore the following to be present in `.env`:

```
SUPABASE_URL=<supabase_project_url>
SUPABASE_KEY=<supabase_anon_key>
```

## Acknowledgement
This code base is built upon the following awesome open-source projects:
- [Stable DreamFusion](https://github.com/ashawkey/stable-dreamfusion)
- [threestudio](https://github.com/threestudio-project/threestudio)
- [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)
- [splat](https://github.com/antimatter15/splat)
- [Point-E](https://github.com/openai/point-e/issues)
- [Shap-E](https://github.com/openai/shap-e)
- [Make-it-3D](https://github.com/junshutang/Make-It-3D)

Thank the authors for their remarkable job !
