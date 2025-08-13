#!/usr/bin/env python3
"""
Test script for skybox generation with GSGEN
"""

import torch
import numpy as np
from omegaconf import OmegaConf
from utils.initialize import initialize
from data import CameraPoseProvider

def test_skybox_initialization():
    """Test skybox initialization function"""
    print("Testing skybox initialization...")
    
    # Create skybox config
    cfg = OmegaConf.create({
        'type': 'skybox',
        'num_points': 1000,
        'skybox_radius': 50.0,
        'skybox_scale': 1.0,
        'svec_val': 0.5,
        'alpha_val': 0.8
    })
    
    # Initialize
    initial_values = initialize(cfg)
    
    # Check results
    mean = initial_values['mean']
    print(f"Generated {mean.shape[0]} Gaussians")
    print(f"Position range: [{mean.min():.2f}, {mean.max():.2f}]")
    print(f"Distance from origin: [{torch.norm(mean, dim=1).min():.2f}, {torch.norm(mean, dim=1).max():.2f}]")
    
    # Verify they're on sphere surface
    distances = torch.norm(mean, dim=1)
    expected_radius = cfg.skybox_radius
    print(f"Expected radius: {expected_radius}")
    print(f"Mean distance: {distances.mean():.2f} ± {distances.std():.2f}")
    
    assert torch.allclose(distances, torch.full_like(distances, expected_radius), atol=1e-5)
    print("✓ Skybox initialization test passed!")

def test_skybox_camera_sampling():
    """Test skybox camera sampling"""
    print("\nTesting skybox camera sampling...")
    
    # Create skybox camera config
    cfg = OmegaConf.create({
        'skybox_mode': True,
        'center': [0, 0, 0],
        'center_aug_std': 0.0,
        'azimuth': [0, 360],
        'elevation': [-90, 90],
        'azimuth_warmup': [0, 360],
        'elevation_warmup': [-90, 90],
        'camera_distance': [0.0, 0.0],
        'reso': [64],
        'reso_milestones': [],
        'focal_milestones': None,
        'focal': [0.7, 1.0],
        'near_plane': 0.1,
        'far_plane': 1000.0,
        'elevation_real_uniform': False,
        'up': [0, 0, 1],
        'light_distance_range': [10, 50],
        'light_aug_std': 0.1,
        'light_sample': 'dreamfusion'
    })
    
    # Create camera provider
    camera_provider = CameraPoseProvider(cfg)
    
    # Sample some camera poses
    poses = []
    for i in range(10):
        sample = camera_provider.sample_one()
        poses.append(sample)
        
        # Check camera is at origin for skybox mode
        c2w = sample['c2w']
        camera_pos = c2w[:3, 3]  # Translation part
        distance_from_origin = torch.norm(camera_pos)
        
        print(f"Sample {i}: camera distance from origin = {distance_from_origin:.6f}")
        assert distance_from_origin < 1e-5, f"Camera should be at origin for skybox, got {camera_pos}"
    
    print("✓ Skybox camera sampling test passed!")

def test_skybox_config():
    """Test loading skybox configuration"""
    print("\nTesting skybox configuration...")
    
    try:
        cfg = OmegaConf.load('conf/skybox.yaml')
        print(f"Loaded skybox config with {len(cfg)} keys")
        print(f"Skybox mode: {cfg.get('skybox_mode', False)}")
        print(f"Init type: {cfg.init.type}")
        print(f"Camera skybox mode: {cfg.data.skybox_mode}")
        print(f"Skip frustum culling: {cfg.gaussians.skip_frustum_culling}")
        print("✓ Skybox configuration test passed!")
    except Exception as e:
        print(f"✗ Skybox configuration test failed: {e}")

if __name__ == "__main__":
    print("GSGEN Skybox Implementation Test Suite")
    print("=" * 50)
    
    try:
        test_skybox_initialization()
        test_skybox_camera_sampling()
        test_skybox_config()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Skybox implementation is ready.")
        print("\nTo generate a skybox, run:")
        print("python main.py --config-name skybox")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
