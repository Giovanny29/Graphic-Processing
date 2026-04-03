#include "../Vetor.h"
#include "../Ponto.h"
#include <string>
#include <vector>
#include <map>
using namespace std;


struct CameraData {
    Ponto lookfrom;
    Ponto lookat;
    Vetor upVector = Vetor(0, 1, 0);
    
    int image_width;
    int image_height;
};


struct ColorData {
    double r, g, b;
    ColorData(){}
    ColorData(double r, double g, double b) : r(r), g(g), b(b) {}
};


struct LightData {
    Ponto       pos;
    ColorData   color;
    map<string, string> extraData;
};


struct MaterialData {
    string    name;
    ColorData color;  // Difuso      (kd)
    ColorData ks;     // Especular   (ks)
    ColorData ka;     // Ambiente    (ka)
    ColorData kr;     // Reflexivo   (kr)  [Emissivo (ke)]
    ColorData kt;     // Transmicivo (kt)
    double    ns;     // Rugosidade  (eta) [Brilho]
    double    ni;     // Refração 
    double    d;      // Opacidade
};


struct ObjectData {
    string objType;     // sphere, plane, mesh, (custom?) ...
    
    Ponto relativePos = Ponto(0, 0, 0);
    MaterialData material;
    
    map<string, double> numericData;
    map<string, Vetor>  vetorPointData;
    map<string, string> otherProperties;
    
    //transformData; ...

    double  getNum     (string key){ return numericData[key]; }
    int64_t getInt     (string key){ return (int64_t)numericData[key]; }
    Vetor   getVetor   (string key){ return vetorPointData[key]; }
    Ponto   getPonto   (string key){ auto p = vetorPointData[key]; return Ponto(p.getZ(), p.getY(), p.getZ()); }
    string  getProperty(string key){ return otherProperties[key]; }
};


struct Scene {
    CameraData camera;
    
    LightData globalLight;
    vector<LightData> lightList;

    vector<ObjectData> objects;
};