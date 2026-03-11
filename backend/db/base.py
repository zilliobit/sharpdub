from db.database import Base 
# Import your models so they "register" themselves onto that Base
from apps.auth.models import User, Role, UserRole, BackupCode

from apps.todos.models import Todo

