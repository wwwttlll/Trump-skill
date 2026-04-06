"""
Trump Species Sprites - 从 JSON 文件加载 ASCII 动画
"""

import sys

# Windows 下设置 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import json
from pathlib import Path

# 加载 JSON 数据
def load_sprites() -> dict:
    """从 JSON 文件加载 sprites 数据"""
    data_path = Path(__file__).parent.parent / "data" / "trump_sprites.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 懒加载
_TRUMP_SPRITES = None

def _get_sprites() -> dict:
    global _TRUMP_SPRITES
    if _TRUMP_SPRITES is None:
        _TRUMP_SPRITES = load_sprites()
    return _TRUMP_SPRITES

# ===== 公开 API =====

def get_sprite(species: str) -> dict:
    """获取指定species的图案数据"""
    sprites = _get_sprites()
    return sprites.get(species, sprites['golfer'])


def render_sprite(species: str, frame: int = 0) -> str:
    """渲染指定species的ASCII图案"""
    sprite_data = get_sprite(species)
    frames = sprite_data.get('frames', [])
    if not frames:
        return ""
    # 保证 frame 在范围内（环绕）
    frame_idx = frame % len(frames)
    # 将单帧的多行列表拼成单个字符串，便于打印
    frame_lines = frames[frame_idx]
    # 计算最长行长度，对齐所有行
    max_len = max(len(line) for line in frame_lines)
    padded_lines = [line.ljust(max_len) for line in frame_lines]
    return "\n".join(padded_lines)


def get_frame_count(species: str) -> int:
    """获取帧数"""
    sprite_data = get_sprite(species)
    return len(sprite_data.get('frames', []))


def get_all_species() -> list:
    """获取所有species列表"""
    return list(_get_sprites().keys())


if __name__ == "__main__":
    import random

    sprites = _get_sprites()
    for species in sprites:
        data = sprites[species]
        max_idx = max(0, len(data.get('frames', [])) - 1)
        frame = random.randint(0, max_idx)
        print(f"\n=== {data['name']} (frame {frame}) ===")
        print(render_sprite(species, frame))
