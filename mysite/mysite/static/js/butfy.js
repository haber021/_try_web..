    // Initialize canvas
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    resizeCanvas();

    window.addEventListener('resize', resizeCanvas);

    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    // Butterfly class
    function Butterfly(x, y, size, speed) {
      this.x = x;
      this.y = y;
      this.size = size;
      this.speed = speed;
      this.angle = Math.random() * Math.PI * 2;
    }

    Butterfly.prototype.draw = function() {
      ctx.save();
      ctx.beginPath();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.angle);
      ctx.fillStyle = 'pink'; // You can change color as per your preference
      ctx.moveTo(0, 0);
      ctx.lineTo(10, -5); // Change shape here
      ctx.lineTo(15, 5);  // Change shape here
      ctx.lineTo(10, 10); // Change shape here
      ctx.lineTo(0, 0);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    };

    Butterfly.prototype.update = function() {
      this.x += Math.cos(this.angle) * this.speed;
      this.y += Math.sin(this.angle) * this.speed;

      // Wrap around edges
      if (this.x < 0) this.x = canvas.width;
      if (this.x > canvas.width) this.x = 0;
      if (this.y < 0) this.y = canvas.height;
      if (this.y > canvas.height) this.y = 0;
    };

    // Create butterflies
    var butterflies = [];
    for (var i = 0; i < 20; i++) {
      var butterfly = new Butterfly(
        Math.random() * canvas.width,
        Math.random() * canvas.height,
        Math.random() * 10 + 5, // Random size between 5 and 15
        Math.random() * 2 + 1   // Random speed between 1 and 3
      );
      butterflies.push(butterfly);
    }

    // Animation loop
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (var i = 0; i < butterflies.length; i++) {
        butterflies[i].update();
        butterflies[i].draw();
      }

      requestAnimationFrame(animate);
    }

    animate();