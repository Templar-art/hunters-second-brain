// Rotating 3D dumbbell for the end card (@remotion/three). Pure function of time.
import React from 'react';
import { ThreeCanvas } from '@remotion/three';

const LIME = '#C3F067', STEEL = '#DDE3DC', DARK = '#56625B';

function Plate({ x, r, w }) {
  return (
    <mesh position={[x, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
      <cylinderGeometry args={[r, r, w, 48]} />
      <meshStandardMaterial color={DARK} metalness={0.3} roughness={0.5} />
    </mesh>
  );
}

export function Dumbbell3D({ t }) {
  const intro = Math.min(1, t / 0.9);
  const ease = 1 - (1 - intro) ** 3;
  return (
    <ThreeCanvas width={1080} height={640} camera={{ position: [0, 0.6, 6], fov: 35 }}>
      <ambientLight intensity={0.9} />
      <directionalLight position={[-4, 2, -3]} intensity={1.2} color="#ffffff" />
      <directionalLight position={[3, 4, 5]} intensity={1.6} />
      <pointLight position={[-4, -2, 3]} intensity={30} color={LIME} />
      <group rotation={[0.35 + Math.sin(t * 1.2) * 0.08, t * 1.1 - (1 - ease) * 2.5, 0.25]} scale={0.4 + 0.6 * ease}>
        <mesh rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.09, 0.09, 3.2, 24]} />
          <meshStandardMaterial color={STEEL} metalness={0.9} roughness={0.25} />
        </mesh>
        {[-1, 1].map((s) => (
          <group key={s}>
            <Plate x={s * 0.9} r={0.78} w={0.22} />
            <Plate x={s * 1.14} r={0.62} w={0.2} />
            <mesh position={[s * 1.32, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
              <cylinderGeometry args={[0.16, 0.16, 0.12, 24]} />
              <meshStandardMaterial color={LIME} metalness={0.2} roughness={0.4} />
            </mesh>
          </group>
        ))}
      </group>
    </ThreeCanvas>
  );
}
