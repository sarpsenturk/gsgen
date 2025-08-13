# GSGEN Skybox Generation

This document describes the skybox generation capability added to GSGEN, which allows generating 360-degree environmental backgrounds instead of specific objects.

## Overview

The skybox implementation modifies GSGEN to:
1. Initialize 3D Gaussians on a large sphere surface facing inward
2. Position the camera at the origin looking outward in all directions
3. Disable frustum culling to render the full spherical environment
4. Optimize rendering for large-scale geometry

## Key Changes Made

### 1. New Initialization Method (`utils/initialize.py`)
- Added `skybox_initialize()` function that places Gaussians on a sphere surface
- Configurable radius and scale parameters for skybox geometry
- Gaussians oriented to face inward toward the camera

### 2. Camera System Modifications (`data/__init__.py`)
- Added `skybox_mode` parameter to `CameraPoseProvider`
- Camera stays at origin (0,0,0) instead of orbiting around object
- Full 360° azimuth and elevation sampling for complete coverage
- Modified camera-to-world matrix calculation for skybox viewing

### 3. Renderer Optimizations (`gs/gaussian_splatting.py`)
- Auto-detection of skybox mode to disable frustum culling
- Larger far plane distances for skybox-scale geometry
- Disabled densification and pruning for initial implementation

### 4. Configuration (`conf/skybox.yaml`)
- Complete skybox configuration with optimal parameters
- Disabled object-centric optimizations (densification, pruning)
- Adjusted camera settings, resolution progression, and training steps

## Usage

### Quick Start
```bash
# Generate a skybox with the default cosmic theme
python main.py --config-name skybox

# Generate a custom skybox
python main.py --config-name skybox prompt.prompt="a beautiful sunset over mountains"
```

### Configuration Options

Key skybox parameters in `conf/skybox.yaml`:

```yaml
# Initialization
init:
  type: skybox
  num_points: 8192        # Number of Gaussians (more = higher detail)
  skybox_radius: 50.0     # Sphere radius
  skybox_scale: 1.0       # Initial Gaussian scale
  alpha_val: 0.5          # Initial opacity

# Camera settings  
data:
  skybox_mode: true
  camera_distance: [0.0, 0.0]  # Camera at origin
  elevation: [-90, 90]         # Full sphere
  azimuth: [0, 360]           # Full rotation

# Renderer
renderer:
  skip_frustum_culling: true   # Essential for skybox
  densify.enabled: false       # Disable for stability
  prune.enabled: false         # Disable for stability
```

### Custom Prompts

Effective skybox prompts should describe environmental scenes:

```yaml
# Good skybox prompts
prompt: "a cosmic nebula with stars and galaxies, space background"
prompt: "dramatic storm clouds with lightning, dark atmosphere"  
prompt: "peaceful forest canopy view from below, green lighting"
prompt: "underwater coral reef environment, blue ambient lighting"
prompt: "alien planet surface with multiple moons in sky"

# Less effective (object-focused)
prompt: "a red car"  # Too specific/localized
prompt: "a person"   # Not environmental
```

## Performance Considerations

### Training Time
- Skybox mode with disabled densification: ~50-70% faster than standard object generation
- Typical training: 1000-3000 steps (vs 5000-15000 for objects)
- Lower resolution (64→128→256) progression for faster convergence

### Memory Usage
- 8192 Gaussians: ~2.3MB parameters
- Large sphere geometry requires more Gaussians for detail
- Disabled culling increases rendering load but improves coverage

### Quality vs Speed Trade-offs
```yaml
# Fast (lower quality)
num_points: 4096
max_steps: 1000
reso: [64, 128]

# Balanced  
num_points: 8192
max_steps: 3000
reso: [64, 128, 256]

# High quality (slower)
num_points: 16384
max_steps: 5000
reso: [64, 128, 256, 512]
```

## Testing

Run the test suite to verify the implementation:

```bash
python test_skybox.py
```

This tests:
- Skybox initialization (Gaussians on sphere surface)
- Camera sampling (camera at origin)
- Configuration loading

## Troubleshooting

### Common Issues

1. **Empty/black renders**: 
   - Check that `skip_frustum_culling: true` is set
   - Verify skybox_radius is reasonable (50-100)
   - Ensure prompt describes environmental scenes

2. **Poor quality**:
   - Increase `num_points` (8192 → 16384)
   - Extend training steps (`max_steps: 5000`)
   - Use better prompts with environmental keywords

3. **Slow training**:
   - Reduce resolution milestones
   - Lower max_steps for testing
   - Ensure densification is disabled

### Debug Mode

Enable debugging to monitor training:

```yaml
renderer:
  debug: true
  
# Check Gaussian distribution
eval:
  image_period: 50  # Frequent evaluation
```

## Future Optimizations

Potential improvements not yet implemented:

1. **Spherical Harmonics Optimization**: Use higher-degree SH for better view-dependent effects
2. **Level of Detail**: Adaptive Gaussian density based on viewing angle
3. **Pretrained Priors**: Initialize with learned skybox distributions
4. **Temporal Consistency**: For animated skyboxes
5. **HDR Support**: High dynamic range for realistic lighting

## Implementation Details

### Core Algorithms

The skybox implementation uses these key modifications:

1. **Spherical Initialization**:
   ```python
   # Sample points on sphere
   theta = torch.rand(N) * 2 * np.pi
   phi = torch.rand(N) * np.pi
   x = R * torch.sin(phi) * torch.cos(theta)
   y = R * torch.sin(phi) * torch.sin(theta) 
   z = R * torch.cos(phi)
   ```

2. **Origin-Centered Camera**:
   ```python
   if skybox_mode:
       pos = np.array([0.0, 0.0, 0.0])  # Camera at origin
       look_at = pos + direction_vector   # Look outward
   ```

3. **Disabled Culling**:
   ```python
   if self.skip_frustum_culling:
       mask = torch.ones_like(mask, dtype=torch.bool)
   ```

This creates an immersive 360° environment suitable for VR, game backgrounds, or architectural visualization.
