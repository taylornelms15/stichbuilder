#include "stitchmainwindow.h"
#include "./ui_stitchmainwindow.h"

StitchMainWindow::StitchMainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::StitchMainWindow)
{
    ui->setupUi(this);
}

StitchMainWindow::~StitchMainWindow()
{
    delete ui;
}

