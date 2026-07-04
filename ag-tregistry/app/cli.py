import argparse
from collections.abc import Sequence

from app.db.session import SessionLocal, init_db
from app.schemas.catalog import DeploymentCreate
from app.services.catalog import CatalogService


def _print_lines(values: Sequence[str]) -> None:
    for value in values:
        print(value)


def main() -> None:
    parser = argparse.ArgumentParser(prog="aa", description="ag-tregistry runtime bridge CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-agents")
    subparsers.add_parser("list-skills")
    subparsers.add_parser("list-mcps")
    subparsers.add_parser("list-prompts")
    subparsers.add_parser("list-deployments")

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("resource_type", choices=("agent", "mcp"))
    deploy_parser.add_argument("resource_name")
    deploy_parser.add_argument("--tag", default="latest")
    deploy_parser.add_argument("--runtime", default="local")
    deploy_parser.add_argument("--namespace", default="default")

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("name")
    remove_parser.add_argument("--namespace", default="default")

    args = parser.parse_args()
    init_db()

    if args.command == "list-agents":
        _print_lines([item["agent"]["name"] for item in CatalogService().list_agents()])
        return
    if args.command == "list-skills":
        _print_lines([item["skill"]["name"] for item in CatalogService().list_skills()])
        return
    if args.command == "list-mcps":
        _print_lines([item["server"]["name"] for item in CatalogService().list_servers()])
        return
    if args.command == "list-prompts":
        _print_lines([item["prompt"]["name"] for item in CatalogService().list_prompts()])
        return

    with SessionLocal() as session:
        service = CatalogService(session)
        if args.command == "list-deployments":
            _print_lines(
                [
                    f"{item.metadata.namespace}/{item.metadata.name}"
                    f" -> {item.spec.target_ref.kind}:{item.spec.target_ref.name}"
                    for item in service.list_deployments(namespace="all")
                ]
            )
            return
        if args.command == "deploy":
            deployment = service.create_deployment(
                DeploymentCreate(
                    resourceType=args.resource_type,
                    resourceName=args.resource_name,
                    tag=args.tag,
                    runtimeId=args.runtime,
                    namespace=args.namespace,
                )
            )
            print(f"deployed {deployment.metadata.namespace}/{deployment.metadata.name}")
            return
        if args.command == "remove":
            result = service.delete_deployment(args.name, namespace=args.namespace)
            print(result.message)
