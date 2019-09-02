#include <iostream>
#include <fstream>

#include <f2c.h>

using namespace std;

// dgeev_ is a symbol in the LAPACK library files
extern "C" {
extern int dgeev_(char*,char*,integer*,double*,integer*,double*, double*, double*, integer*, double*, integer*, double*, integer*, integer*);
}

int main(int argc, const char* argv[])
{
  std::string fileName;
  // check for an argument
  if (argc<2){
    fileName = "matrix.txt";
    //cout << "Usage: " << argv[0] << " " << " filename" << endl;
    //return -1;
  }
  else
  {
    fileName = argv[1];
  }
  

  integer n,m;
  double *data;

  // read in a text file that contains a real matrix stored in column major format
  // but read it into row major format
  ifstream fin(fileName.c_str());
  if (!fin.is_open()){
    cout << "Failed to open " << argv[1] << endl;
    return -1;
  }
  fin >> n >> m;  // n is the number of rows, m the number of columns
  data = new double[n*m];
  for (integer i=0;i<n;i++){
    for (integer j=0;j<m;j++){
      fin >> data[j*n+i];
    }
  }
  if (fin.fail() || fin.eof()){
    cout << "Error while reading " << argv[1] << endl;
    return -1;
  }
  fin.close();

  // check that matrix is square
  if (n != m){
    cout << "Matrix is not square" <<endl;
    return -1;
  }

  // allocate data
  char Nchar='N';
  double *eigReal=new double[n];
  double *eigImag=new double[n];
  double *vl,*vr;
  integer one=1;
  integer lwork=6*n;
  double *work=new double[lwork];
  integer info;

  // calculate eigenvalues using the DGEEV subroutine
  dgeev_(&Nchar,&Nchar,&n,data,&n,eigReal,eigImag,
        vl,&one,vr,&one,
        work,&lwork,&info);


  // check for errors
  if (info!=0){
    cout << "Error: dgeev returned error code " << info << endl;
    return -1;
  }

  // output eigenvalues to stdout
  cout << "--- Eigenvalues ---" << endl;
  for (int i=0;i<n;i++){
    cout << "( " << eigReal[i] << " , " << eigImag[i] << " )\n";
  }
  cout << endl;

  // deallocate
  delete [] data;
  delete [] eigReal;
  delete [] eigImag;
  delete [] work;


  return 0;
}