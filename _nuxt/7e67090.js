(window.webpackJsonp=window.webpackJsonp||[]).push([[23],{1045:function(t,e,n){"use strict";n.d(e,"b",(function(){return r})),n.d(e,"a",(function(){return c}));var o=n(95),r=Object(o.c)("dashboardParameters",{state:function(){return{codeSampleParameter:!1}},actions:{setCodeSampleParameter:function(t){this.codeSampleParameter=t}}}),c=Object(o.c)("dAppParameters",{state:function(){return{payWithOption:"XRT",currentDrawingSegments:[]}}})},1204:function(t,e,n){var content=n(1372);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(57).default)("e204229a",content,!0,{sourceMap:!1})},1368:function(t,e){},1370:function(t,e){},1371:function(t,e,n){"use strict";n(1204)},1372:function(t,e,n){var o=n(56)((function(i){return i[1]}));o.push([t.i,".canvas-style[data-v-a93bab18]{cursor:crosshair;width:100%!important;height:300px!important;display:block;margin:auto;background-color:#ffedd5}",""]),o.locals={},t.exports=o},1383:function(t,e,n){"use strict";n.r(e);var o=n(29),r=(n(21),n(43),n(48),n(37),n(47),n(65),n(66),n(94)),c=n(1045);function l(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,n)}return e}var f=n(1367),d=Object(r.b)({props:["canvasId"],emits:["drawing_sent"],setup:function(t,e){e.emit;var path=null,n=null,d=[],m=Object(c.b)(),v=Object(c.a)();Object(r.d)((function(){(n=new f.PaperScope).setup(t.canvasId)}));var w=function(){v.currentDrawingSegments=[],d.forEach((function(path){var t=[];console.log(path._segments),path._segments.forEach((function(e){t.push([e.point.x,e.point.y])})),v.currentDrawingSegments.push(t)}))};return{mouseDown:function(t){console.log("mouse down");var e=function(t){return console.log("createTool"),t.activate(),new f.Tool}(n);e.onMouseDown=function(t){path=function(t){return t.activate(),new f.Path({strokeColor:"#000000",strokeJoin:"round",strokeWidth:1.5})}(n),path.add(t.point)},e.onMouseDrag=function(t){console.log("mouse drag"),path.add(t)},e.onMouseUp=function(t){console.log("mouse up"),path.add(t.point),path.simplify(10),path.flatten(3),d.push(function(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?l(Object(source),!0).forEach((function(e){Object(o.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):l(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}({},path)),console.log(d),w()}},resetCanvas:function(){m.setCodeSampleParameter(!1),n.project.activeLayer.removeChildren(),d=[],w()}}}}),m=d,v=(n(1371),n(25)),component=Object(v.a)(m,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{staticClass:"w-full mb-8"},[n("canvas",{staticClass:"canvas-style",attrs:{id:t.canvasId},on:{mousedown:t.mouseDown}})]),t._v(" "),n("button",{staticClass:"uppercase text-md w-full py-2 my-2 px-4 bg-gray-200 text-gray-800\n      hover:bg-gray-800 hover:bg-gray-100 hover:text-white",attrs:{type:"button"},on:{click:t.resetCanvas}},[t._v("\n    Clear canvas\n  ")])])}),[],!1,null,"a93bab18",null);e.default=component.exports}}]);