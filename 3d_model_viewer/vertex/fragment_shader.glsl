#version 120
varying vec3 vNormal;
uniform vec3 lightDir;
void main() {
    float diffuse = max(dot(normalize(vNormal), normalize(lightDir)), 0.0);
    if (diffuse < 0.13) diffuse = 0.13; // жорстка тінь, змінюй як треба
    gl_FragColor = vec4(vec3(0.65, 0.65, 0.65) * diffuse, 1.0);
}
