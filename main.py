import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# No modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.")
        return code


class UrbanRoutesPage:
    """Clase que representa la página de rutas urbanas."""

    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button =(By.CSS_SELECTOR, '.button.round') #
    comfort_tariff_option = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']") #//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]

    # Register Phone
    phone_button = (By.CLASS_NAME, "np-button")
    phone_field = (By.ID, 'phone')
    phone_code = (By.ID, "code")
    phone_next_button = (By.XPATH, "//button[@class='button full' and text()='Siguiente']")
    phone_sms_field = (By.ID, "code")
    phone_sms_confirmation_button = (By.XPATH, "//button[@class='button full' and text()='Confirmar']")

    # Register Credit card
    add_card_button = (By.XPATH, "//div[@class='pp-row disabled']//div[@class='pp-title' and text()='Agregar tarjeta']")
    type_of_pay_button = (By.XPATH, "//div[@class='pp-button filled']//div[@class='pp-text' and text()='Método de pago']")
    add_confirm_card_button = (By.XPATH, "//button[text()='Agregar']")
    card_number_field = (By.ID, 'number')
    card_code_field = (By.XPATH, "//input[@id='code' and @name='code' and @placeholder='12']")  # CVV
    confirm_card_button = (By.ID, 'link')


    message_box = (By.XPATH, '//input[@id="comment"]')
    blanket_and_tissues_checkbox = (By.XPATH, "(//input[@class='switch-input'])[1]")

    #(//input[@class='switch-input'])[1]
    #tissues_checkbox = (By.ID, 'tissues')
    ice_cream_plus_button = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div[@class='r-counter']//div[@class='counter-plus']")
    ice_cream_value = (By.XPATH, "//div[contains(text(), 'Helado')]/following-sibling::div//div[@class='counter-value']")

    request__taxi_button = (By.XPATH, "//button[contains(@class, 'smart-button') and .//span[contains(@class, 'smart-button-main')]]")
    taxi_modal = (By.XPATH, "//div[contains(@class, 'order-header-content')]//div[contains(text(), 'Buscar automóvil')]")

    def __init__(self, driver):
        self.driver = driver

    # ---------------------- SETTERS ----------------------
    def set_from(self, from_address):
        """Ingresa la dirección de origen."""
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        """Ingresa la dirección de destino."""
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.to_field)).send_keys(to_address)

    def set_phone(self, phone_number):
        """Ingresa el número de teléfono."""
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.phone_field)).send_keys(phone_number)

    def set_message_to_driver(self, message):
        """Escribe un mensaje para el conductor."""
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.message_box)).send_keys(message)

    def set_phone_sms(self):
        """Obtiene y confirma el código de teléfono."""
        phone_code = retrieve_phone_code(self.driver)
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.phone_sms_field)).send_keys(phone_code)

    def set_card_number(self, card_number):
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.card_number_field)).send_keys(card_number)

    def set_card_number_loss_focus(self):
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.card_number_field)).send_keys(Keys.TAB)

    def set_card_code(self, code):
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.card_code_field)).send_keys(code)

    def set_card_code_loss_focus(self):
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.card_code_field)).send_keys(Keys.TAB)

    def set_scroll_down_ice_cream(self):
        checkbox = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(self.ice_cream_plus_button)
        )

        # Hacer scroll hasta el checkbox para que sea visible
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)

    def set_ice_cream_counter_button(self, quantity):
        for _ in range(quantity):
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.ice_cream_plus_button)).click()

    # ---------------------- GETTERS ----------------------
    def get_from(self):
        """Obtiene la dirección de origen ingresada."""
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        """Obtiene la dirección de destino ingresada."""
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_phone(self):
        """Obtiene el número de teléfono ingresado."""
        return self.driver.find_element(*self.phone_field).get_property('value')

    def get_message(self):
        """Obtiene el mensaje ingresado para el conductor."""
        return self.driver.find_element(*self.message_box).get_property('value')

    def get_request_taxi_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.request_taxi_button))

    def get__request_taxi_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.request__taxi_button))

    def get_comfort_tariff_option(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.comfort_tariff_option))

    def get_phone_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.phone_button))

    def get_phone_next_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.phone_next_button))

    def get_phone_sms_confirm_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.phone_sms_confirmation_button))

    def get_type_of_pay_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.type_of_pay_button))

    def get_add_credit_card_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.add_card_button))

    def get_confirm_add_credit_card_button(self):
        return WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.add_confirm_card_button))

    def get_blanket_and_tissues_checkbox(self):
        """Hace scroll y hace clic en el checkbox de Manta y Pañuelos, asegurando que sea clickeable."""

        # Esperar a que el checkbox esté presente en el DOM
        checkbox = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(self.blanket_and_tissues_checkbox)
        )

        # Hacer scroll hasta el checkbox para que sea visible
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)

        # Intentar hacer click normalmente, si falla usar JavaScript
        try:
            checkbox.click()
            print("Checkbox clickeado normalmente")
        except:
            self.driver.execute_script("arguments[0].click();", checkbox)
            print("Checkbox clickeado con JavaScript")

        return  checkbox

    def get_ice_cream_value(self):
        #ice_cream_count = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID,'//div[@class="r-counter-label" and text()="Chocolate"]/ancestor::div[@class="r-counter-container"]'))).text
        ice_cream_count = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(self.ice_cream_value)).text
        return  ice_cream_count


    def get_verify_taxi_modal_appears(self):
        """Verifica que aparece el modal para buscar un taxi."""
        return WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(self.taxi_modal))

    # ---------------------- MÉTODOS DE ACCIÓN ----------------------
    def select_comfort_tariff(self):
        """Selecciona la tarifa Comfort."""
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.comfort_tariff_option)).click()

    def click_on_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def click_on_comfort_tariff_option(self):
        self.get_comfort_tariff_option().click()

    def add_credit_card(self, card_number, cvv):
        """Agrega una tarjeta de crédito."""
        #WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.add_card_button)).click()

        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.card_number_field)).send_keys(card_number)

        cvv_field = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.card_code_field))
        cvv_field.send_keys(cvv)
        cvv_field.send_keys(Keys.TAB)  # Cambiar el enfoque para activar el botón de confirmación
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.confirm_card_button)).click()


    def request_ice_cream(self, quantity=2):
        """Pide helados según la cantidad especificada."""
        for _ in range(quantity):
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.ice_cream_plus_button)).click()






class TestUrbanRoutes:
    """Clase de pruebas automatizadas en Selenium."""

    driver = None

    @classmethod
    def setup_class(cls):
        """Configura el driver de Selenium."""
        options = Options()
        options.set_capability("goog:loggingPrefs",{'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(),options=options)

    @classmethod
    def teardown_class(cls):
        """Cierra el navegador después de las pruebas."""
        cls.driver.quit()

    def test_set_route(self):
        """ Configurar direcciones"""
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        assert routes_page.get_from() == data.address_from, "Error: La dirección de origen no se ingresó correctamente."
        assert routes_page.get_to() == data.address_to, "Error: La dirección de destino no se ingresó correctamente."

    def test_select_comfort(self):
        """Seleccionar tarifa Comfort"""
        self.test_set_route()
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_on_request_taxi_button()
        routes_page.select_comfort_tariff()

        comfort_button_exist = routes_page.get_comfort_tariff_option().text
        comfort_text = "Comfort"
        assert comfort_button_exist in comfort_text

    def test_fill_telephone_number(self):
        """Llenar el campo telefono"""
        self.test_select_comfort()
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.get_phone_button().click()
        routes_page.set_phone(data.phone_number)
        routes_page.get_phone_next_button().click()

        routes_page.set_phone_sms()
        routes_page.get_phone_sms_confirm_button().click()

        assert routes_page.get_phone() == data.phone_number, "Error: El número de teléfono ingresado no es correcto."


    def test_add_credit_card(self):
        """Agregar tarjeta de crédito"""
        self.test_select_comfort()
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.get_type_of_pay_button().click()
        routes_page.get_add_credit_card_button().click()
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.set_card_code_loss_focus()
        routes_page.get_confirm_add_credit_card_button().click()

        card_element = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.XPATH, "//div[@class='pp-row']//div[@class='pp-title' and text()='Tarjeta']"))
        )

        assert card_element is not None, "Error: El elemento 'Tarjeta' no existe en la página."

    def test_send_message_to_driver(self):
        """Escribir mensaje para el conductor """
        self.test_select_comfort()
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_message_to_driver(data.message_for_driver)
        assert routes_page.get_message() == data.message_for_driver, "Error: El mensaje para el conductor no coincide."

    def test_request_blanket_and_tissues(self):
        """Pedir manta y pañuelos"""
        self.test_select_comfort()
        routes_page = UrbanRoutesPage(self.driver)

        # 🔹 Hacer scroll directamente hasta el checkbox
       # blanket_and_tissues_checkbox = routes_page.get_blanket_and_tissues_checkbox()
        #self.driver.execute_script("arguments[0].scrollIntoView(true);", blanket_and_tissues_checkbox)

        routes_page.get_blanket_and_tissues_checkbox()

        #routes_page.request_blanket_and_tissues()
        # Verificar que los checkboxes están seleccionados
        blanket_and_tissues_selected = self.driver.find_element(*routes_page.blanket_and_tissues_checkbox).is_selected()
        assert blanket_and_tissues_selected, "Error: La manta no está seleccionada."


    def test_request_ice_cream(self):
        self.test_select_comfort()
        routes_page = UrbanRoutesPage(self.driver)
        # Pedir 2 helados de chocolate
        routes_page.set_scroll_down_ice_cream()
        routes_page.set_ice_cream_counter_button(2)
        #routes_page.request_ice_cream(2)

        # Verificar que se añadieron 2 helados (asumimos que hay un contador visible)
        ice_cream_count = routes_page.get_ice_cream_value()
        assert ice_cream_count == "2", "Error: No se agregaron 2 helados correctamente."

    def test_modal_looking_for_taxi(self):
        self.test_fill_telephone_number()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message_to_driver(data.message_for_driver)

        routes_page.get__request_taxi_button().click()
        modal_element = routes_page.get_verify_taxi_modal_appears()

        assert modal_element is not None, "Error: Modal 'Buscando taxi...' no aparece."