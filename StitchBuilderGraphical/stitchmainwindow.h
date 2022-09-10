#ifndef STITCHMAINWINDOW_H
#define STITCHMAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class StitchMainWindow; }
QT_END_NAMESPACE

class StitchMainWindow : public QMainWindow
{
    Q_OBJECT

public:
    StitchMainWindow(QWidget *parent = nullptr);
    ~StitchMainWindow();

private:
    Ui::StitchMainWindow *ui;
};
#endif // STITCHMAINWINDOW_H
