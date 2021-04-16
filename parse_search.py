from utils import database
from utils import utils



if __name__ == '__main__':

    vacancies = utils.parse_title("JS Dev")
    database.update_vacancies(vacancies)

