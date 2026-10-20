"""Bird flight simulation shared by the Blender build and the auto-layout router.

Pure numpy (runs in system Python and in Blender's Python). A bird is a dict:
  depth       m from the camera at frame 1
  sx, sy      start screen offset from centre in px (+y up)
  speed       m/s
  hz          wingbeat frequency
  phase       starting beat phase (cycles)
  heading     mid-shot heading, deg: 0 = screen right, +90 = straight away from camera
  bank        deg, far wing raised (drone sees the back); also sets the turn rate
  span        wingspan m
  glides      [[t0, t1], ...] seconds; t0 <= 0 means "gliding from the start"
simulate() returns keys every KEY_STEP frames with world position, euler (XYZ) and wing pose.
"""
import math
import numpy as np

TOP, BOT, DOWN = 50.0, -28.0, 0.58  # arm elevation range (deg); downstroke = 58% of the beat
GLIDE = dict(elev=6.0, arm_sweep=6.0, hand_dih=-6.0, hand_sweep=12.0, twist=0.0)
SUB = 4
KEY_STEP = 0.5
G = 9.81


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def elev(u):
    """Arm elevation through one beat: slow powered downstroke, quick recovery."""
    u %= 1.0
    if u < DOWN:
        return TOP + (BOT - TOP) * (1 - math.cos(math.pi * u / DOWN)) / 2
    return BOT + (TOP - BOT) * (1 - math.cos(math.pi * (u - DOWN) / (1 - DOWN))) / 2


def w_up(u):
    u %= 1.0
    return math.sin(math.pi * (u - DOWN) / (1 - DOWN)) if u >= DOWN else 0.0


def w_dn(u):
    u %= 1.0
    return math.sin(math.pi * u / DOWN) if u < DOWN else 0.0


def glide_w(t, windows, ramp=0.15):
    g = 0.0
    for a, b in windows:
        on = 1.0 if a <= 0 else smooth((t - a) / ramp)
        g = max(g, on * (1 - smooth((t - b) / ramp)))
    return g


def cam_basis(M1):
    """Horizontal right / forward vectors of the frame-1 camera (Blender camera: -Z forward)."""
    R = np.asarray(M1)[:3, :3]
    right = R @ np.array([1.0, 0, 0]); right[2] = 0; right /= np.linalg.norm(right)
    fwd = R @ np.array([0, 0, -1.0]); fwd[2] = 0; fwd /= np.linalg.norm(fwd)
    return right, fwd


def start_pos(bird, M1, f_px):
    d = bird["depth"]
    p_cam = np.array([bird["sx"] / f_px * d, bird["sy"] / f_px * d, -d, 1.0])
    return (np.asarray(M1) @ p_cam)[:3]


def simulate(bird, M1, f_px, fps, n_frames):
    right, fwd = cam_basis(M1)
    speed, span, bank = bird["speed"], bird["span"], bird["bank"]
    glides = bird.get("glides", [])
    t_shot = (n_frames - 1) / fps
    omega0 = G * math.tan(math.radians(bank)) / speed
    ang = math.radians(bird["heading"]) + omega0 * t_shot / 2  # mid-shot heading == requested
    pos = start_pos(bird, M1, f_px)
    phase, t, frame, next_key = bird.get("phase", 0.0), 0.0, 1.0, 1.0
    dt = 1 / (fps * SUB)
    seed = bird.get("phase", 0.0) * 6
    keys = []
    while frame <= n_frames + 1e-6:
        g = glide_w(t, glides)
        u = phase % 1.0
        roll = bank + 2.0 * math.sin(1.3 * t + seed)
        if frame >= next_key - 1e-6:
            fl = dict(elev=elev(u), arm_sweep=14 * w_up(u),
                      hand_dih=0.55 * (elev(u - 0.07) - elev(u)) - 4,
                      hand_sweep=40 * w_up(u), twist=-9 * w_dn(u))
            pose = {k: (1 - g) * fl[k] + g * GLIDE[k] for k in fl}
            lowness = (TOP - elev(u - 0.22)) / (TOP - BOT)  # body lifts as the wings come down
            lift = (1 - g) * 0.05 * span * (lowness - 0.5)
            dirv = right * math.cos(ang) + fwd * math.sin(ang)
            heading = math.atan2(dirv[1], dirv[0]) - math.pi / 2  # local +Y faces travel
            keys.append(dict(
                frame=next_key,
                pos=(pos + np.array([0, 0, lift])).tolist(),
                euler=[math.radians(-4 + 2.5 * (1 - g) * w_dn(u) - 1.5 * g), math.radians(roll), heading],
                wings=pose))
            next_key += KEY_STEP
        v = speed * ((1 - g) * (1 + 0.05 * w_dn(u)) + g * 0.97)
        dirv = right * math.cos(ang) + fwd * math.sin(ang)
        pos = pos + dirv * v * dt + np.array([0, 0, ((1 - g) * 0.25 - g * 0.7) * dt])
        ang -= G * math.tan(math.radians(roll)) / v * dt  # right wing low -> turn right
        phase += bird["hz"] * (1 - g) * dt
        t += dt
        frame += 1 / SUB
    return keys


def project(p, M, f_px, w, h):
    """World point -> pixel (x right, y down) for a Blender camera matrix. Returns (x, y, depth)."""
    Minv = np.linalg.inv(np.asarray(M))
    c = Minv @ np.array([*p, 1.0])
    z = -c[2]
    if z <= 0.05:
        return None
    return (f_px * c[0] / z + w / 2, h / 2 - f_px * c[1] / z, z)
