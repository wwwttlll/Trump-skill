import sys

# Windows 下设置 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from typing import Tuple
from tools.trump_sprites import get_frame_count

# FNV-1a 哈希算法
def fnv1a_32(data: str) -> int:
    """FNV-1a 32位哈希"""
    h = 2166136261
    for byte in data.encode('utf-8'):
        h ^= byte
        h = (h * 16777619) & 0xFFFFFFFF
    return h

# Mulberry32 伪随机数生成器
def mulberry32(seed: int):
    """Mulberry32 PRNG"""
    a = seed & 0xFFFFFFFF
    def next_float():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = (a ^ (a >> 15)) * (1 | a)
        t = (t + (t ^ (t >> 7)) * (61 | t)) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return next_float

# 8种 Species
SPECIES = [
    'golfer',
    'executive_pen',
    'truth_social',
    'media_enemy',
    'biden_hunter',
    'china_tariff',
    'election_stolen',
    'self_contradiction',
]

# 时间段
TIME_BASED_SPECIES = {
    'morning': 'golfer',
    'afternoon': 'executive_pen',
    'evening': 'truth_social',
}

def get_time_of_day() -> str:
    """获取当前时间段"""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    else:
        return 'evening'

def get_salt() -> str:
    """获取今日盐值 (trump-YYYY-MM)"""
    now = datetime.now()
    return f"trump-{now.year}-{now.month:02d}"

def detect_trump_species(user_message: str = "", user_id: str = "default") -> Tuple[str, dict]:
    """
    基于用户消息+时间哈希确定 species

    使用 buddy 系统的确定性随机：
    1. 盐值 = trump-YYYY-MM (每月变化)
    2. 用户消息 + 盐值 → FNV-1a 哈希
    3. 哈希 → Mulberry32 种子
    4. PRNG 依次选择: species → frame
    """
    # 1. 获取盐值
    salt = get_salt()

    # 2. 构建哈希输入 (用户消息 + 盐值)
    # 如果没有用户消息，使用时间段作为默认
    if user_message.strip():
        hash_input = f"{user_id}:{user_message}:{salt}"
    else:

        time_of_day = get_time_of_day()
        species = TIME_BASED_SPECIES[time_of_day]

        time_hash_input = f"default:{time_of_day}:{salt}"
        seed = fnv1a_32(time_hash_input)
        return species, {
            'reason': 'time_based',
            'time_of_day': time_of_day,
            'salt': salt,
            'hash_input': time_hash_input,
            'seed': seed,
        }

    seed = fnv1a_32(hash_input)

    rng = mulberry32(seed)

    species_index = int(rng() * len(SPECIES))
    species = SPECIES[species_index]

    # 确保选取的帧索引不会越界（以 sprites 中的帧数为准）
    frame_count = get_frame_count(species)
    frame_index = int(rng() * max(1, frame_count))

    return species, {
        'reason': 'hash_based',
        'salt': salt,
        'hash_input': hash_input,
        'seed': seed,
        'species_index': species_index,
        'frame': frame_index,
    }

def get_species_info(species: str) -> dict:
    """获取species详细信息"""
    from tools.trump_sprites import load_sprites

    sprites = load_sprites()
    sprite_data = sprites.get(species, sprites['golfer'])

    species_keywords = {
        'golfer': 'golf, club, tee',
        'executive_pen': 'order, sign, executive',
        'truth_social': 'truth, post, social',
        'media_enemy': 'fake news, media, cnn',
        'biden_hunter': 'biden, hunter, corrupt',
        'china_tariff': 'china, tariff, trade',
        'election_stolen': 'election, stolen, fraud',
        'self_contradiction': 'flip, contradict',
    }

    return {
        'name': sprite_data['name'],
        'description': sprite_data['description'],
        'keywords': species_keywords.get(species, []),
    }

# CLI测试
if __name__ == "__main__":
    import sys

    # 测试不同消息
    messages = [
        "你好",
        "今天天气怎么样",
        "关于中国",
        "拜登太差了",
        "",
    ]

    print(f"=== 今日盐值: {get_salt()} ===\n")

    for msg in messages:
        species, info = detect_trump_species(msg)
        print(f"Message: '{msg}'")
        print(f"  Reason: {info['reason']}")
        if 'hash_input' in info:
            print(f"  Input: {info['hash_input']}")
            print(f"  Seed: {info['seed']}")
        print(f"  Species: {species}")
        print()
