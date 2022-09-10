#include "stitchmainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
  QApplication a(argc, argv);
  StitchMainWindow w;
  w.show();
  return a.exec();
}
