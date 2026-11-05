from lisichki.domain.usecases.login import LoginUserUseCase
from lisichki.domain.usecases.messages import ManageMessagesUseCase
from lisichki.domain.usecases.registration import RegistrateUserUseCase
from lisichki.domain.usecases.roles import ManageRolesUseCase

registrate_user: RegistrateUserUseCase
login_user: LoginUserUseCase
manage_roles: ManageRolesUseCase
manage_messages: ManageMessagesUseCase
