#version 330

out vec4 finalColor;

uniform float time;
uniform vec2 resolution;
// uniform vec2 mouse;


void main()
{
    vec4 c = vec4(0.0);
    float l;
    float t = -time;
	vec2 p = gl_FragCoord.xy / resolution.xy *2. - 1.;
	
	p.x *= resolution.x / resolution.y;
	float angle = time * 0.05;
	l = length(p) * pow(pow(2, p.x), p.y) * .6;// * -p.y;
	// p = mat2(cos(angle), -sin(angle), sin(angle),  cos(angle)) * p;
	for (int i = 0; i < 4; ++i) {
		t+=.3;
		c[i] = (0.02 / smoothstep(abs(sin(l * 8. + t)/8.)- .2, pow(p.y, l), pow(p.x / 1000, l)));
	}
    finalColor = vec4(c);
}
