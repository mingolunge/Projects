#version 330

out vec4 finalColor;

uniform float time;
uniform vec2 resolution;
uniform vec2 zoom;
uniform vec2 mouse;
uniform vec2 co;
uniform vec2 offset;
uniform vec2 center;


void main()
{
    float xtemp;
    vec4 color = vec4(0.0);

    vec2 p = gl_FragCoord.xy / resolution.xy * 2.0 - 1.0;
    p.x *= resolution.x / resolution.y;	

    p = p * zoom + offset + center;

    float R = 2.0;
    float i = 0.0;
	    float m_i = 300.0;

    vec2 z = p;

    while (z.x * z.x + z.y * z.y < R * R && i < m_i) {
        xtemp = z.x * z.x - z.y * z.y;
        z.y = 2.0 * z.x * z.y + co.y;
        z.x = xtemp + co.x;
        i += 1.0;
    }

    i /= m_i;
    float t = i;

    vec3 cA = vec3(t, t, t / 3.0);
    vec3 cB = vec3(t, t / 2.0, t);
    vec3 cC = vec3(t, t, t);
    vec3 cD = vec3(t, t, t);

    vec3 col;

    if (t < 0.25) {
        col = cA;
    } else if (t < 0.4) {
        col = mix(cA, cB, smoothstep(0.25, 0.4, t));
    } else if (t < 0.65) {
        col = mix(cB, cC, smoothstep(0.4, 0.65, t));
    } else {
        col = mix(cC, cD, smoothstep(0.65, 1.0, t));
    }

    finalColor = vec4(col, 1.0);
}
