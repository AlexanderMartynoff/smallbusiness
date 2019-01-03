from typing import List, Any, Dict


class AuthorizationPolicy:
    def checkpermission(self, permission: str, usercontext: Dict[str, Any]):
        raise NotImplementedError
