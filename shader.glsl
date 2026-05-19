#begin vertex
#version 330
in vec2 in_position;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}


#begin fragment
#version 330

uniform float zoom;
uniform vec2 offset;

const int iterations = 256;

vec2 complex_mult( vec2 v0, vec2 v1 ) {
    // (a + bi) * (c + di) = a*c - d*b + (a*d + c*b)*i
    return vec2(
        v0.x*v1.x - v0.y*v1.y,
        v0.x*v1.y + v0.y*v1.x
    );
}

float mandlebrot( vec2 c ) {
    vec2 z = vec2(0);
    for ( int i = 0; i < iterations; i++ )
        z = complex_mult(z,z) + c;
    
    float v = abs( z.x * z.y );
    return v < 1000.0 ? 1.0 : 0.0;
}




void main() {
    vec2 pos = gl_FragCoord.xy * 0.0027 - vec2(2, 1);
    float v = mandlebrot(pos * zoom + offset);

    gl_FragColor = vec4(v, v, v, 1.0);
}