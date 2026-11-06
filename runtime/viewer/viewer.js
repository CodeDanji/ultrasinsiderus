import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const stage=document.querySelector('#stage');
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0xf0f5f3);
renderer.toneMapping=THREE.ACESFilmicToneMapping;stage.appendChild(renderer.domElement);
const scene=new THREE.Scene();scene.add(new THREE.HemisphereLight(0xffffff,0xb6c6be,2));
for(const [position,power] of [[[1,2,2],3],[[-1,1,-1],1.5]]){const light=new THREE.DirectionalLight(0xffffff,power);light.position.set(...position);scene.add(light)}
const camera=new THREE.OrthographicCamera(-1,1,1,-1,.001,10);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
let center=new THREE.Vector3(),size=.3;
const groups={bones:[],muscles:[],vessels:[],fat:[]};
function resize(){renderer.setSize(stage.clientWidth,stage.clientHeight);const aspect=stage.clientWidth/stage.clientHeight,span=size*.65;camera.left=-span*aspect;camera.right=span*aspect;camera.top=span;camera.bottom=-span;camera.updateProjectionMatrix()}
function reset(){camera.position.copy(center).add(new THREE.Vector3(0,0,1.5).multiplyScalar(size));controls.target.copy(center);resize();controls.update()}
addEventListener('resize',resize);resize();
const raw=atob(document.querySelector('#model-data').textContent.trim());const bytes=Uint8Array.from(raw,c=>c.charCodeAt(0));
new GLTFLoader().parse(bytes.buffer,'',gltf=>{scene.add(gltf.scene);const box=new THREE.Box3().setFromObject(gltf.scene);center=box.getCenter(new THREE.Vector3());size=Math.max(...box.getSize(new THREE.Vector3()).toArray());gltf.scene.traverse(obj=>{if(!obj.isMesh)return;const name=obj.name.toLowerCase(),material=(obj.material?.name||'').toLowerCase();const kind=name.includes('fat')?'fat':name.includes('arteries')?'vessels':material.startsWith('muscle')?'muscles':'bones';groups[kind].push(obj);obj.visible=document.querySelector(`[data-layer="${kind}"]`).checked});reset();document.querySelector('#loading').hidden=true;document.querySelector('#ready').textContent='드래그하여 회전 · 휠/두 손가락으로 확대';window.viewerReady=true},error=>{document.querySelector('#loading').textContent='모형을 열 수 없습니다. GLB 파일을 지원 프로그램에서 확인해 주세요.';console.error(error)});
for(const input of document.querySelectorAll('[data-layer]'))input.addEventListener('change',()=>groups[input.dataset.layer].forEach(obj=>obj.visible=input.checked));
document.querySelector('#reset').onclick=reset;
document.querySelector('#download').onclick=()=>{const a=document.createElement('a'),url=URL.createObjectURL(new Blob([bytes],{type:'model/gltf-binary'}));a.href=url;a.download='foot-model.glb';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
function animate(){requestAnimationFrame(animate);controls.update();renderer.render(scene,camera)}animate();
