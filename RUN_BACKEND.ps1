# سكريبت تشغيل خادم Django
# Run Django Backend Server

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  جامعة العين - Server Startup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# الانتقال إلى مجلد Backend
Set-Location "$PSScriptRoot\backend"

# التحقق من وجود virtualenv
if (Test-Path "venv") {
    Write-Host "✓ Virtual Environment موجود" -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠ Virtual Environment غير موجود" -ForegroundColor Yellow
    Write-Host "اقم بتشغيل: python -m venv venv" -ForegroundColor Yellow
}

# التحقق من قاعدة البيانات
if (Test-Path "db.sqlite3") {
    Write-Host "✓ Database موجودة" -ForegroundColor Green
} else {
    Write-Host "⚠ Database غير موجودة" -ForegroundColor Yellow
    Write-Host "اقم بتشغيل: python manage.py migrate" -ForegroundColor Yellow
}

# عرض معلومات التشغيل
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Server Information" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Frontend URL: http://localhost:8000" -ForegroundColor Blue
Write-Host "📡 API Base URL: http://localhost:8000/api" -ForegroundColor Blue
Write-Host "🔧 Admin Panel: http://localhost:8000/admin" -ForegroundColor Blue
Write-Host ""
Write-Host "✨ اضغط Ctrl+C لإيقاف الخادم" -ForegroundColor Yellow
Write-Host ""

# تشغيل الخادم
python manage.py runserver 0.0.0.0:8000
