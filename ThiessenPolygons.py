# -*- coding: utf-8 -*-

import arcpy

# تنظیم محیط کاری
arcpy.env.overwriteOutput = True

try:
    # دریافت پارامترها از ابزار
    input_points = arcpy.GetParameterAsText(0)
    threshold_area = float(arcpy.GetParameterAsText(1))
    output_folder = arcpy.GetParameterAsText(2)

    # تنظیم فایل‌های خروجی
    output_polygons = output_folder + "\\Thiessen_Polygons.shp"
    output_filtered = output_folder + "\\Filtered_Polygons.shp"

    # تولید پلیگون‌های تیسن
    arcpy.AddMessage("در حال ایجاد پلیگون‌های تیسن...")
    arcpy.analysis.CreateThiessenPolygons(input_points, output_polygons, "ALL")

    # اضافه کردن فیلد مساحت
    arcpy.AddMessage("در حال اضافه کردن فیلد مساحت...")
    arcpy.management.AddField(output_polygons, "Area", "DOUBLE")

    # محاسبه مساحت برای هر پلیگون
    arcpy.AddMessage("در حال محاسبه مساحت...")
    arcpy.CalculateField_management(
        output_polygons, "Area", "!shape.area@METERS!", "PYTHON_9.3"
    )

    # ساخت یک کوئری برای انتخاب پلیگون‌ها با مساحت بیشتر از حد آستانه
    where_clause = '"Area" > {}'.format(threshold_area)
    arcpy.AddMessage("در حال فیلتر کردن پلیگون‌ها...")
    arcpy.analysis.Select(output_polygons, output_filtered, where_clause)

    arcpy.AddMessage("ابزار با موفقیت اجرا شد!")
    arcpy.AddMessage("خروجی‌ها ذخیره شدند در: {}".format(output_filtered))

except arcpy.ExecuteError:
    arcpy.AddError("خطای ArcPy: {}".format(arcpy.GetMessages(2)))
    print(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddError("خطای عمومی: {}".format(str(e)))
    print(str(e))

