// node inspect_glb.mjs a.glb [b.glb ...]  -> JSON lines: decodes EXT_meshopt_compression and reports counts/bounds
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { getBounds } from '@gltf-transform/functions';
import { MeshoptDecoder } from 'meshoptimizer';
await MeshoptDecoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder });
for (const f of process.argv.slice(2)) {
  const doc = await io.read(f);
  const root = doc.getRoot();
  let verts = 0, tris = 0;
  for (const m of root.listMeshes()) for (const p of m.listPrimitives()) {
    verts += p.getAttribute('POSITION')?.getCount() ?? 0;
    tris += (p.getIndices()?.getCount() ?? 0) / 3;
  }
  const b = getBounds(root.getDefaultScene() ?? root.listScenes()[0]);
  console.log(JSON.stringify({ file: f, nodes: root.listNodes().length, meshes: root.listMeshes().length, vertices: verts, triangles: Math.round(tris),
    bounds_mm: [b.min.map((v) => +(v * 1000).toFixed(3)), b.max.map((v) => +(v * 1000).toFixed(3))], extensions: root.listExtensionsUsed().map((e) => e.extensionName) }));
}
