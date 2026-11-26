// Usage: node optimize_glb.mjs in.glb out.glb [--wrap]
// KiCad/OCC GLBs carry one primitive per B-rep face (10k+ primitives). This merges primitives that share a
// material INSIDE each mesh (node tree and node names are untouched), dedups accessors, then applies
// gltf-transform's meshopt transform (reorder + quantize + EXT_meshopt_compression, level high).
// --wrap: footprint nodes that own a mesh get it moved to a child node first, because quantization rewrites
// the transform of mesh-bearing nodes and would otherwise shift the footprint origin.
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { dedup, meshopt, prune, joinPrimitives } from '@gltf-transform/functions';
import { MeshoptEncoder, MeshoptDecoder } from 'meshoptimizer';

const [, , inp, out, ...flags] = process.argv;
await MeshoptEncoder.ready; await MeshoptDecoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.encoder': MeshoptEncoder, 'meshopt.decoder': MeshoptDecoder });
const doc = await io.read(inp);
const root = doc.getRoot();

if (flags.includes('--wrap')) {
  for (const node of root.listNodes()) {
    const mesh = node.getMesh();
    if (mesh && node.getName()) {
      const child = doc.createNode(node.getName() + '__mesh').setMesh(mesh);
      node.setMesh(null).addChild(child);
    }
  }
}
for (const mesh of root.listMeshes()) {
  const groups = new Map();
  for (const p of mesh.listPrimitives()) {
    const key = [p.getMaterial()?.getName() ?? '', root.listMaterials().indexOf(p.getMaterial()), p.getMode(), p.listSemantics().sort().join(',')].join('|');
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(p);
  }
  for (const prims of groups.values()) {
    if (prims.length < 2) continue;
    const joined = joinPrimitives(prims);
    prims.forEach((p) => { mesh.removePrimitive(p); p.dispose(); });
    mesh.addPrimitive(joined);
  }
}
await doc.transform(prune(), dedup(), meshopt({ encoder: MeshoptEncoder, level: 'high' }));
await io.write(out, doc);
