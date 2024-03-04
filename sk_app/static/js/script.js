import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const scene = new THREE.Scene();
// 背景色
scene.background = new THREE.Color( 0x000000 );

// 初期設定
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);


// 前右、上下から光を当てるライトを作成
const frontLight = new THREE.DirectionalLight(0xffffff, 1);
const rightLight = new THREE.DirectionalLight(0xffffff, 1);
const leftLight = new THREE.DirectionalLight(0xffffff, 1);
const backLight = new THREE.DirectionalLight(0xffffff, 1);
const topLight = new THREE.DirectionalLight(0xffffff, 1);
const bottomLight = new THREE.DirectionalLight(0xffffff, 1);

// ライトの位置を設定
frontLight.position.set(0, 0, 1);
rightLight.position.set(1, 0, 0);
topLight.position.set(0, 1, 0);
bottomLight.position.set(0, -1, 0);
backLight.position.set(0, 0, -1);
leftLight.position.set(-1, 0, 0);

// 光の強度を増やす
frontLight.intensity = 1;
rightLight.intensity = 1;

// シーンにライトを追加
scene.add(frontLight);
scene.add(rightLight);
scene.add(backLight);
scene.add(leftLight);
// scene.add(topLight);
// scene.add(bottomLight);


// Ajaxリクエストを作成し、データを受信
$.ajax({
    // pythonからデータを受け取る
    type: 'GET',
    url: '/model_data',
    success: function(response) {
        console.log(response);
        const loader = new GLTFLoader();
        loader.load('../static/uploads/models/'+response, function (gltf) {
            const models=gltf.scene
            // モデルをシーンに追加
            scene.add(models);
            // カメラの位置と方向を変更して正面から表示する  
            models.rotation.x = Math.PI / 2;
            models.rotation.z = Math.PI / 2;
            // モデルを少し横に移動させる
            models.position.x = 0.5;
            // Ajaxリクエストを作成し、データを受信
            $.ajax({
                // pythonからデータを受け取る
                type: 'GET',
                url: '/mediapipe_data',
                success: function(response) {
                    console.log(response);
                    if (response.key1=="OK") {
                        // OKであれば回転１
                        rotateModel1();
                    }else if (data.mediapipe_data=="FALSE"){
                        // FALSEであれば回転2
                        rotateModel2();
                    }
                }
            });
                
        
            // マウスクリック時に押下した方向にモデルを回転
            document.addEventListener('mousedown', onMouseEvent, false);
            function onMouseEvent(event){
                if (mouse>=window.innerWidth/2){
                    rotateModel1();// 回転
                    // scaleUp();// 拡大
                }else{
                    rotateModel2();// 回転
                    // scaleDown();// 縮小
                    window.location.href='/projection';// エンドポイント呼び出し（ページ遷移用）
                }
            }
        
            // マウスを離したら
            document.addEventListener('mouseup', onMouseUp);
            function onMouseUp(){
                stopAnimation();
            }
            let animationFrameId;
            // モデルを回転させる関数
            function rotateModel1() {
                // モデルのy軸を中心に回転
                models.rotation.x += -0.01;
                // モデルを再描画
                renderer.render(scene, camera);
                // アニメーションを繰り返し実行
                animationFrameId = requestAnimationFrame(rotateModel1);
            }
            // モデルを回転させる関数(ボツ)
            function rotateModel2() {
                models.rotation.x += 0.01;
                renderer.render(scene, camera);
                animationFrameId = requestAnimationFrame(rotateModel2);
            }
            // アニメーションを停止する関数         停止させたい場合はこれを呼び出す
            function stopAnimation() {
                cancelAnimationFrame(animationFrameId);
                cancelAnimationFrame(animationId);
            }
            let animationId
            // 拡大する関数
            function scaleUp(event) {   
                // フレームごとに実行される関数
                function render() {
                  // オブジェクトのスケールを変更
                  models.scale.x += 0.05;
                  models.scale.y += 0.05;
                  models.scale.z += 0.05;
                  // フレームごとに実行される関数を再帰的に呼び出す
                  animationId = requestAnimationFrame(render);
                  console.log(camera.position);
                }
                render()
            }
            // 縮小する関数
            function scaleDown(event) {
                // フレームごとに実行される関数
                function render() {
                    // オブジェクトのスケールを変更
                    models.scale.x += -0.05;
                    models.scale.y += -0.05;
                    models.scale.z += -0.05;
                    // フレームごとに実行される関数を再帰的に呼び出す
                    animationId = requestAnimationFrame(render);
                }
                render()
            }
        }, undefined, function (error) {
            console.error(error);
        }); 
    }
});



// コントローラーセット
const controls = new OrbitControls(camera, renderer.domElement);
controls.autoRotate = false; //trueだとカメラが自動回転
// controls.autoRotate = true;
// 滑らかにカメラコントローラーを制御する
controls.enableDamping = true;
controls.dampingFactor = 0.2;
controls.update();


// カメラの位置変更
camera.position.y = 1;
camera.position.z = 5;



// 毎フレーム時に実行されるループイベントです
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();


let mouse = 0; // マウス座標
// マウス座標はマウスが動いた時のみ取得できる
document.addEventListener("mousemove", (event) => {
    mouse = event.pageX;
});
