$(document).ready(function(){
  var colorPicker = new iro.ColorPicker('#color-picker',{
    width: 600,
    color: $('#active-color').html(),
    sliderSize: 75,
    layoutDirection: "horizontal",
    layout: [
    { 
      component: iro.ui.Wheel
    },
    { 
      component: iro.ui.Slider
    },
  ]
  });

  $('.button').click(function(){
    $.post('/animation', {type: $(this).attr('data-type')}, function(data){
      console.log(data);
    }, 'json');
  })

  colorPicker.on('color:change', function(color) {
    // log the current color as a HEX string
    $('#rgb').html(color.red + "," + color.green + "," + color.blue);
    $.post('/color-change', {r: color.red, g: color.green, b: color.blue}, function(data){
       console.log(data);
    }, 'json');
  });
});
