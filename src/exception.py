import sys
from src.logger import logging
def error_message_detail(error: BaseException) -> str:
    exc_type, exc_value, exc_tb = sys.exc_info()
    if exc_tb is None:
        # Fallback if called outside an except block
        return f"error message [{error}]"
    file_name = exc_tb.tb_frame.f_code.co_filename
    return ("Error occurred in python script name [{0}] "
            "line number [{1}] error message [{2}]").format(
                file_name, exc_tb.tb_lineno, str(error))
    
    
class CustomException(Exception):
    def __init__(self, original_error: BaseException):
        detailed = error_message_detail(original_error)
        super().__init__(detailed)
        self.original_error = original_error  # optional: keep original

    def __str__(self) -> str:
        return super().__str__()
    

#if __name__=="__main__":
#    try:
#        a=1/0
#    except Exception as e:
#        logging.info("Divide by zero")
#        raise CustomException(e)    