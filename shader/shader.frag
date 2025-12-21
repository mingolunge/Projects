#version 330

out vec4 finalColor;

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;

vec3 palette(float t)
{
    vec3 colors[10] = vec3[](
        vec3(0.0, 87.0, 0.0) / 255.0,
        vec3(0.0, 0.0, 255.0) / 255.0,
        vec3(255.0, 0.0, 0.0) / 255.0,
        vec3(0.0, 255.0, 0.0) / 255.0,
        vec3(13.0, 134.0, 255.0) / 255.0,
        vec3(251.0, 9.0, 195.0) / 255.0,
        vec3(255.0, 182.0, 172.0) / 255.0,
        vec3(255.0, 225.0, 0.0) / 255.0,
        vec3(37.0, 0.0, 26.0) / 255.0,
        vec3(0.0, 255.0, 255.0) / 255.0
    );

    float x = fract(t * 0.1) * 10.0;
    int i0 = int(floor(x));
    int i1 = (i0 + 1) % 10;
    float f = fract(x);

    return mix(colors[i0], colors[i1], f);
}


void main()
{
    vec3 c = vec3(0.0);
    float l;
    float t = time;
	vec2 p = gl_FragCoord.xy / resolution.xy *2. - .1;
	vec2 p0 = p;
	p.x *= resolution.x / resolution.y;
	// p = (fract(p *1.5) -.5);
	// p.x -= mouse.x;
	// p.y += mouse.y;
	l = length(p);
	vec3 col = palette(time);
	l = sin(l*8 + time) / 8;
	l = abs(l);
	
	l = 0.02 / l;

	// for (int i = 0; i < 3; ++i) {
	// 	t+=.1;
	// 	c[i] = 0.02 / abs(sin(l * 8. + t)/4.) - (abs(mouse.x / 20)) +.2;
	// }
    finalColor = vec4(l/ col, 1.);
}
