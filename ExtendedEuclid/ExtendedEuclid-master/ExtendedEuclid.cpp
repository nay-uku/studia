#include <iostream>
#include <cstdio>
#include <cmath>
using namespace std;
typedef long long int llong;

//extended Euclid
void gcd_ee(llong a, llong b)
{
    llong gcd, q, ua, ub, r1, r2, u, v, pa, pua;
    ua = 1;
    ub = 0;
    r1 = a;
    r2 = b;

    while (r2 != 0) {
        q = r1 / r2;

        pua = ua; //help variable for ua
        ua = ub;

        pa = r1; //help variable for r1
        r1 = r2;

        ub = pua - q * ub;
        r2 = pa - q * r2;
        cout << r1 << " = " << ua << " * " << a << " + " << (r1 - ua * a) / b << " * " << b << endl;
    }
    gcd = r1;
    u = ua;
    v = (gcd - u * a) / b;
    cout << "\ngcd(a,b)= " << gcd << " = " << u << " * " << a << " + " << v << " * " << b << endl;

    cout << "\nGCD = " << gcd << endl
         << "u, v : " << u << ", " << v << endl
         << endl;
}
int main()
{
    llong a, b, temp;
    cout << "Type a and b to count GCD: \n";
    cin >> a >> b;
    if(b > a){
    	temp=a;
    	a=b;
    	b=temp;
    }
    cout<<endl;
    gcd_ee(a, b);
    cout << "Press enter to continue ...";
    cin.get();
    cin.get();

    return 0;
}
