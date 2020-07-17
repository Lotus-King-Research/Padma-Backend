function renderWords(dict) {
  var data = dict

  DeadSimpleRenderer = function(canvas){
    var canvas = $(canvas).get(0)
    var ctx = canvas.getContext("2d");
    var particleSystem = null

    var that = {

      init:function(system){
        
        particleSystem = system

        particleSystem.screenSize(canvas.width, canvas.height) 
        particleSystem.screenPadding(80)
      },
      
      redraw:function(){
        ctx.clearRect(0,0, canvas.width, canvas.height)
        
        particleSystem.eachEdge(function(edge, pt1, pt2){

          ctx.strokeStyle = "rgba(0, 0, 0, .05)"
          ctx.lineWidth = 1 + 4*edge.data.weight
          ctx.beginPath()
          ctx.moveTo(pt1.x, pt1.y)
          ctx.lineTo(pt2.x, pt2.y)
          ctx.stroke()
        })

        particleSystem.eachNode(function(node, pt){
          var w = ctx.measureText(node.data.label||"").width + 6
          var label = node.data.label

          if (!(label||"").match(/^[ \t]*$/)){
            pt.x = Math.floor(pt.x)
            pt.y = Math.floor(pt.y)
          } else {
            label = 'སེམས་ཉིད་'
          }

          
          ctx.clearRect(pt.x-w/2, pt.y-7, w,14)

          if (label){
            ctx.font = "bold 36px Arial"
            ctx.textAlign = "center"

            ctx.fillStyle = "rgba(0, 0, 0, .5)"

            ctx.fillText(label||"", pt.x, pt.y+4)
          }
        })  			
      }
    }
    return that
  }    

  $(document).ready(function(){
    var sys = arbor.ParticleSystem(1000, 800, 0.5) 
    sys.renderer = DeadSimpleRenderer("#viewport")
    sys.graft({nodes:data.nodes, edges:data.edges})
    
    $("a.another").click( function(){ 
      window.location.reload(); 
      return false 
    })
  })

}(this.jQuery)