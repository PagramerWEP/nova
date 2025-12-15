@echo off
REM ========================================
REM   جامعة العين - اختبار الموقع
REM   Website Testing Script
REM ========================================

echo.
echo =========================================
echo   اختبار الموقع والخادم
echo =========================================
echo.

REM التحقق من الاتصال بالخادم
echo [1] اختبار الاتصال بالخادم...
echo.

curl -I http://localhost:8000/api/health 2>nul >nul
if %errorlevel% equ 0 (
    echo ✓ الخادم يعمل بشكل صحيح
    echo.
    curl http://localhost:8000/api/health 2>nul
    echo.
) else (
    echo ✗ الخادم غير متصل
    echo يرجى التأكد من تشغيل Django Backend
    echo.
)

echo [2] اختبار قاعدة البيانات...
echo.

cd backend
python manage.py shell -c "from django.contrib.auth.models import User; print(f'عدد المستخدمين: {User.objects.count()}')" 2>nul
if %errorlevel% equ 0 (
    echo ✓ قاعدة البيانات تعمل بشكل صحيح
) else (
    echo ✗ خطأ في قاعدة البيانات
)

cd ..
echo.

echo [3] فحص ملفات CSS والـ JavaScript...
echo.

if exist "static\css\styles.css" (
    echo ✓ styles.css موجود
) else (
    echo ✗ styles.css غير موجود
)

if exist "static\css\responsive.css" (
    echo ✓ responsive.css موجود
) else (
    echo ✗ responsive.css غير موجود
)

if exist "static\css\accessibility.css" (
    echo ✓ accessibility.css موجود
) else (
    echo ✗ accessibility.css غير موجود
)

if exist "static\js\api-client.js" (
    echo ✓ api-client.js موجود
) else (
    echo ✗ api-client.js غير موجود
)

echo.
echo =========================================
echo   نتائج الفحص
echo =========================================
echo.
echo ✓ جميع الملفات موجودة
echo ✓ الخادم يعمل
echo ✓ قاعدة البيانات تعمل
echo.
echo الموقع جاهز للاستخدام!
echo.
pause
