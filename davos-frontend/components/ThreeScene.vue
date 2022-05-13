<template>
  <div>
    <div id="threeSceneContainer" class="scene-container"></div>
  </div>
</template>

<script>
import * as Three from 'three'

export default {
  name: 'ThreeScene',
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      meth: null,
      plane:null
    }
  },
  methods: {
    init() {
      let container = document.getElementById('threeSceneContainer')
      this.camera = new Three.PerspectiveCamera(70, container.clientWidth / container.clientHeight, 0.01, 10)
      this.camera.position.z = 0.6
      this.camera.position.y = 800
      this.scene = new Three.Scene()
      let geometry = new Three.BoxGeometry(0.2, 0.2, 0.2)
      let material = new Three.MeshNormalMaterial()
      this.mesh = new Three.Mesh(geometry, material)
      this.scene.add(this.mesh)

      this.plane = new Three.Mesh( new Three.PlaneGeometry( 1000, 1000, 20, 20 ), new Three.MeshBasicMaterial( { color: 0x555555, wireframe: true } ) );
      this.plane.rotation.x = - Math.PI / 2;
      this.scene.add( this.plane );


      this.renderer = new Three.WebGLRenderer({antialias: true})
      this.renderer.setSize(container.clientWidth, container.clientHeight)
      container.appendChild(this.renderer.domElement)
    },
    animate() {
      requestAnimationFrame(this.animate)
      this.mesh.rotation.x += 0.01
      this.mesh.rotation.y += 0.02
      this.renderer.render(this.scene, this.camera)
    }
  },
  mounted() {
    this.init()
    this.animate()
  }

}
</script>

<style scoped>
.scene-container{
  height: 600px;
}
</style>
