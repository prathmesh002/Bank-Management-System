from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from bankapp.models import accounts
from bankapp.forms import (
    addaccountsform,
    balanceform,
    withdrawform,
    depositeform,
    transferform,
    closeform
)


# Home Page
def homepage(request):
    return render(request, "home.html")


# Add Account
def addaccounts(request):
    if request.method == "POST":
        form = addaccountsform(request.POST)

        if form.is_valid():
            acc_number = form.cleaned_data["acc_number"]

            if accounts.objects.filter(acc_number=acc_number).exists():
                return render(request, "addaccounts.html", {
                    "form": form,
                    "message": "Account number already exists!"
                })

            account = form.save(commit=False)
            account.password = make_password(account.password)
            account.save()

            return render(request, "addaccounts.html", {
                "form": addaccountsform(),
                "message": "Account created successfully!"
            })
    else:
        form = addaccountsform()

    return render(request, "addaccounts.html", {"form": form})


# Check Balance
def balance(request):
    form = balanceform()
    message = ""
    account = None

    if request.method == "POST":
        form = balanceform(request.POST)

        if form.is_valid():
            acc_number = form.cleaned_data["acc_number"]
            password = form.cleaned_data["password"]

            account = accounts.objects.filter(
                acc_number=acc_number
            ).first()

            if account and check_password(password, account.password):
                message = "Account found successfully!"
            else:
                account = None
                message = "Invalid account number or password!"

    return render(request, "balance.html", {
        "form": form,
        "account": account,
        "message": message
    })


# Withdraw Money
def withdraw(request):
    form = withdrawform()
    message = ""

    if request.method == "POST":
        form = withdrawform(request.POST)

        if form.is_valid():
            acc_number = form.cleaned_data["acc_number"]
            password = form.cleaned_data["password"]
            amount = form.cleaned_data["amount"]

            account = accounts.objects.filter(
                acc_number=acc_number
            ).first()

            if not account or not check_password(
                password, account.password
            ):
                message = "Invalid account number or password!"

            elif account.amount < amount:
                message = "Insufficient balance!"

            else:
                account.amount -= amount
                account.save(update_fields=["amount"])
                message = "Withdrawal successful!"

    return render(request, "withdraw.html", {
        "form": form,
        "message": message
    })


# Deposit Money
def deposite(request):
    form = depositeform()
    message = ""

    if request.method == "POST":
        form = depositeform(request.POST)

        if form.is_valid():
            acc_number = form.cleaned_data["acc_number"]
            amount = form.cleaned_data["amount"]

            account = accounts.objects.filter(
                acc_number=acc_number
            ).first()

            if not account:
                message = "Account does not exist!"

            else:
                account.amount += amount
                account.save(update_fields=["amount"])
                message = "Deposit successful!"

    return render(request, "deposite.html", {
        "form": form,
        "message": message
    })


# Transfer Money
def transfer(request):
    form = transferform()
    message = ""

    if request.method == "POST":
        form = transferform(request.POST)

        if form.is_valid():
            from_acc = form.cleaned_data["from_acc_number"]
            to_acc = form.cleaned_data["to_acc_number"]
            password = form.cleaned_data["password"]
            amount = form.cleaned_data["amount"]

            if from_acc == to_acc:
                message = "Sender and receiver accounts must differ!"

            else:
                try:
                    with transaction.atomic():
                        sender = accounts.objects.select_for_update().get(
                            acc_number=from_acc
                        )
                        receiver = accounts.objects.select_for_update().get(
                            acc_number=to_acc
                        )

                        if not check_password(password, sender.password):
                            message = "Invalid sender password!"

                        elif sender.amount < amount:
                            message = "Insufficient balance!"

                        else:
                            sender.amount -= amount
                            receiver.amount += amount

                            sender.save(update_fields=["amount"])
                            receiver.save(update_fields=["amount"])

                            message = "Transfer successful!"

                except accounts.DoesNotExist:
                    message = "Sender or receiver account does not exist!"

    return render(request, "transfer.html", {
        "form": form,
        "message": message
    })


# Close Account
def close(request):
    form = closeform()
    message = ""

    if request.method == "POST":
        form = closeform(request.POST)

        if form.is_valid():
            acc_number = form.cleaned_data["acc_number"]
            password = form.cleaned_data["password"]

            account = accounts.objects.filter(
                acc_number=acc_number
            ).first()

            if not account or not check_password(
                password, account.password
            ):
                message = "Invalid account number or password!"

            elif account.amount != 0:
                message = "Withdraw or transfer the remaining balance first!"

            else:
                account.delete()
                message = "Account closed successfully!"
                form = closeform()

    return render(request, "close.html", {
        "form": form,
        "message": message
    })