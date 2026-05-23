# =============================================================================
# locators/locators.py
# All locators for Toreja Medical Clinic PMS — Playwright version
# =============================================================================
# In Playwright, locators are strings passed to page.locator()
# Strategies: CSS selectors, XPath, role, text, label
# =============================================================================


class URLs:
    BASE             = "https://torejamedicalclinic.kesug.com"
    LOGIN            = "https://torejamedicalclinic.kesug.com/index.php"
    DASHBOARD        = "https://torejamedicalclinic.kesug.com/dashboard.php"
    NEW_PRESCRIPTION = "https://torejamedicalclinic.kesug.com/new_prescription.php"
    PATIENTS         = "https://torejamedicalclinic.kesug.com/patients.php"
    PATIENT_HISTORY  = "https://torejamedicalclinic.kesug.com/patient_history.php"
    MEDICINES        = "https://torejamedicalclinic.kesug.com/medicines.php"
    MEDICINE_DETAILS = "https://torejamedicalclinic.kesug.com/medicine_details.php"
    REPORTS          = "https://torejamedicalclinic.kesug.com/reports.php"
    USERS            = "https://torejamedicalclinic.kesug.com/users.php"
    LOGOUT           = "https://torejamedicalclinic.kesug.com/logout.php"


class LoginPage:
    USERNAME_INPUT   = "#user_name"
    PASSWORD_INPUT   = "#password"
    LOGIN_BUTTON     = "button[name='login']"
    ERROR_MESSAGE    = "p.text-danger, p[style*='color']"
    LOGO             = "#system-logo"


class NavBar:
    TOGGLE_SIDEBAR       = "a[data-widget='pushmenu']"
    WELCOME_TEXT         = "div.login-user"
    SIDEBAR              = "aside.main-sidebar"
    USER_PANEL_NAME      = "div.user-panel div.info a"

    MENU_DASHBOARD_LINK  = "#mnu_dashboard > a"
    MENU_PATIENTS_LINK   = "#mnu_patients > a"
    MENU_MEDICINES_LINK  = "#mnu_medicines > a"
    MENU_REPORTS_LINK    = "#mnu_reports > a"
    MENU_USERS_LINK      = "#mnu_users > a"

    SUBMENU_NEW_RX       = "#mi_new_prescription"
    SUBMENU_PATIENTS     = "#mi_patients"
    SUBMENU_HISTORY      = "#mi_patient_history"
    SUBMENU_ADD_MED      = "#mi_medicines"
    SUBMENU_MED_DETAILS  = "#mi_medicine_details"
    SUBMENU_REPORTS      = "#mi_reports"

    LOGOUT_LINK          = "a[href='logout.php']"
    FOOTER               = "footer.main-footer"


class DashboardPage:
    PAGE_HEADING  = "section.content-header h1"
    BOX_TODAY     = "div.small-box.bg-info"
    BOX_WEEK      = "div.small-box.bg-purple"
    BOX_MONTH     = "div.small-box.bg-fuchsia"
    BOX_YEAR      = "div.small-box.bg-maroon"
    COUNT_TODAY   = "div.small-box.bg-info h3"
    COUNT_WEEK    = "div.small-box.bg-purple h3"
    COUNT_MONTH   = "div.small-box.bg-fuchsia h3"
    COUNT_YEAR    = "div.small-box.bg-maroon h3"


class PatientsPage:
    PAGE_HEADING        = "section.content-header h1"
    PATIENT_NAME        = "#patient_name"
    ADDRESS             = "#address"
    CNIC                = "#cnic"
    DATE_OF_BIRTH       = "input[name='date_of_birth']"
    PHONE_NUMBER        = "#phone_number"
    GENDER              = "#gender"
    SAVE_BTN            = "#save_Patient"

    TABLE               = "#all_patients"
    SEARCH_INPUT        = "#all_patients_filter input"
    PAGE_INFO           = "#all_patients_info"
    PREV_BTN            = "#all_patients_previous"
    NEXT_BTN            = "#all_patients_next"

    BTN_COPY            = "button:has(span:text('Copy'))"
    BTN_CSV             = "button:has(span:text('CSV'))"
    BTN_EXCEL           = "button:has(span:text('Excel'))"
    BTN_PDF             = "button:has(span:text('PDF'))"
    BTN_PRINT           = "button:has(span:text('Print'))"


class NewPrescriptionPage:
    PAGE_HEADING        = "section.content-header h1"

    # Patient Select2
    PATIENT_SELECT      = "#patient"
    PATIENT_S2_TRIGGER  = "#patient + .select2-container .select2-selection"
    PATIENT_SEARCH      = "input[placeholder='Type Patient Name...']"

    VISIT_DATE          = "[name='visit_date']"
    NEXT_VISIT_DATE     = "[name='next_visit_date']"
    BP_INPUT            = "[name='bp']"
    WEIGHT_INPUT        = "[name='weight']"
    DISEASE_INPUT       = "[name='disease']"

    ADD_ROW_BTN         = "#add_row"
    MEDICATION_TBODY    = "#medication_list"

    MEDICINE_SEARCH     = "input[placeholder='Type Medicine...']"
    FREQUENCY_SELECT    = "[name='frequency[]']"
    TIMING_SELECT       = "[name='timing[]']"
    QTY_INPUT           = "[name='qty[]']"
    DOSAGE_INPUT        = "[name='dosage[]']"

    SAVE_BTN            = "button[name='submit']"

    # Select2 dropdown results
    S2_OPTION           = "li.select2-results__option"
    S2_SEARCHING        = "li.select2-results__option--disabled:has-text('Searching')"


class PatientHistoryPage:
    PAGE_HEADING        = "section.content-header h1"
    PATIENT_SELECT      = "#patient"
    PATIENT_S2_TRIGGER  = "#patient + .select2-container .select2-selection"
    PATIENT_SEARCH      = "input[placeholder='Type Patient Name...']"
    SEARCH_BTN          = "#search"
    TABLE               = "#patient_history"
    HISTORY_TBODY       = "#history_data"
    S2_OPTION           = "li.select2-results__option"
    S2_SEARCHING        = "li.select2-results__option--disabled:has-text('Searching')"


class MedicinesPage:
    PAGE_HEADING        = "section.content-header h1"
    MEDICINE_NAME       = "#medicine_name"
    SAVE_BTN            = "#save_medicine"
    TABLE               = "#all_medicines"
    SEARCH_INPUT        = "#all_medicines_filter input"
    PAGE_INFO           = "#all_medicines_info"


class MedicineDetailsPage:
    PAGE_HEADING        = "section.content-header h1"
    MEDICINE_SELECT     = "#medicine"
    PACKING_INPUT       = "#packing"
    SAVE_BTN            = "#submit"
    TABLE               = "#medicine_details"
    SEARCH_INPUT        = "#medicine_details_filter input"
    PAGE_INFO           = "#medicine_details_info"


class ReportsPage:
    PAGE_HEADING            = "section.content-header h1"
    PATIENTS_FROM           = "#patients_from"
    PATIENTS_TO             = "#patients_to"
    GENERATE_VISITS_PDF     = "#print_visits"
    DISEASE_INPUT           = "#disease"
    DISEASE_FROM            = "#disease_from"
    DISEASE_TO              = "#disease_to"
    GENERATE_DISEASE_PDF    = "#print_diseases"
    VISITS_HEADING          = "h3:has-text('Patient Visits Between Two Dates')"
    DISEASE_HEADING         = "h3:has-text('Disease Based Report Between Two Dates')"


class UsersPage:
    PAGE_HEADING        = "section.content-header h1"
    DISPLAY_NAME        = "#display_name"
    USERNAME            = "#user_name"
    PASSWORD            = "#password"
    PROFILE_PIC         = "#profile_picture"
    SAVE_BTN            = "[name='save_user']"
    TABLE               = "#all_users"
